# || Start of Imports ||
import os
# Python built in library, used to loop through files in the knowledge_base folder
# and build file paths. No installation needed.

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, BSHTMLLoader
# LangChain community loaders for each file type
# PyPDFLoader    → reads PDF files
# Docx2txtLoader → reads Word documents
# BSHTMLLoader   → reads HTML files using BeautifulSoup
# Docs: https://python.langchain.com/docs/integrations/document_loaders/

from langchain.text_splitter import RecursiveCharacterTextSplitter
<<<<<<< HEAD
# Splits large documents into smaller chunks for vector storage
# Docs: https://python.langchain.com/docs/how_to/recursive_text_splitter/

from langchain_chroma import Chroma
# Vector store — stores and searches document chunks as vectors
# Docs: https://python.langchain.com/docs/integrations/vectorstores/chroma/

from langchain_ollama import OllamaEmbeddings, OllamaLLM
# OllamaEmbeddings → converts text chunks into vectors locally using llama3.2
# OllamaLLM       → runs llama3.2 locally for generating disposal instructions
# Docs: https://python.langchain.com/docs/integrations/llms/ollama/

from langchain_core.prompts import ChatPromptTemplate
# Builds reusable prompt templates with variables
# Docs: https://python.langchain.com/docs/concepts/prompt_templates/
# || End of Imports ||


# || Start of Document Loading ||
def load_documents(folder: str) -> list:
    # Function that takes a folder path as a string
    # Returns a flat list of all loaded document sections
    # Called once on startup to load all knowledge base files

    docs = []
    # Empty list that will be filled with loaded document sections

    for filename in os.listdir(folder):
        # os.listdir returns every filename in the folder as a list
        # We loop through each one to check its file type

        filepath = os.path.join(folder, filename)
        # os.path.join builds the full file path
        # folder = "backend/knowledge_base"
        # filename = "recycling_rules.pdf"
        # filepath = "backend/knowledge_base/recycling_rules.pdf"

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            # PyPDFLoader reads each page of the PDF as a separate document
            # Each page becomes its own entry in the docs list

        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(filepath)
            # Docx2txtLoader extracts plain text from Word documents
            # Strips all formatting, keeps just the text content

        elif filename.endswith(".html"):
            loader = BSHTMLLoader(filepath)
            # BSHTMLLoader uses BeautifulSoup to parse HTML
            # Strips HTML tags and keeps readable text content

        else:
            continue
            # Skip any file that is not PDF, DOCX or HTML
            # continue means jump to the next iteration of the loop

        docs.extend(loader.load())
        # loader.load() returns a list of document objects
        # extend() adds all of them to our docs list
        # append() would add the list itself as one item — extend() flattens it

    print(f"Loaded {len(docs)} document sections from {folder}")
    return docs
# || End of Document Loading ||


# || Start of Vector Store ||
def build_vectorstore(docs: list) -> Chroma:
    # Takes the loaded documents and stores them in ChromaDB
    # Returns a Chroma vectorstore object that can be searched later

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    # Splits documents into chunks of 500 characters
    # chunk_size=500 — each chunk is at most 500 characters long
    # chunk_overlap=50 — chunks share 50 characters with the previous chunk
    # Overlap prevents disposal instructions from being cut off mid sentence
    # Example: "Place in recycling bin. Remove the" ← overlap carries this to next chunk
    # Docs: https://python.langchain.com/docs/how_to/recursive_text_splitter/

    chunks = splitter.split_documents(docs)
    # split_documents takes our list of documents and returns a larger list of smaller chunks
    # A 10 page PDF might become 200 chunks of 500 characters each

    print(f"Split into {len(chunks)} chunks")

    embeddings = OllamaEmbeddings(model="llama3.2")
    # OllamaEmbeddings converts each text chunk into a vector
    # A vector is a list of numbers that represents the meaning of the text
    # Similar meaning = similar numbers
    # Example: "recycle plastic bottle" and "put bottle in blue bin" would have similar vectors
    # Uses llama3.2 running locally — no data sent to any external API
    # Docs: https://python.langchain.com/docs/integrations/text_embedding/ollama/

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    # Chroma.from_documents does two things:
    # 1. Converts every chunk into a vector using OllamaEmbeddings
    # 2. Stores all those vectors in ChromaDB for fast similarity search
    # from_documents is a class method — it creates the vectorstore and fills it in one step
    # Docs: https://python.langchain.com/docs/integrations/vectorstores/chroma/

    print("Vector store built successfully")
    return vectorstore
# || End of Vector Store ||


# || Start of Initialization ||
KNOWLEDGE_BASE_PATH = "backend/knowledge_base"
# Path to the folder containing your PDFs, DOCX and HTML files
# Written in all caps because it is a constant — never changes while the program runs

print("Loading knowledge base...")
docs = load_documents(KNOWLEDGE_BASE_PATH)
# Calls load_documents on startup — loads all files once into memory

vectorstore = build_vectorstore(docs)
# Builds the ChromaDB vector store from the loaded documents
# This runs once on startup — expensive operation, don't run on every request

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
# Converts the vectorstore into a retriever object
# as_retriever() gives us a simple interface to search the vectorstore
# search_kwargs={"k": 3} means return the 3 most relevant chunks per search
# k=3 is a balance — enough context for Ollama without overwhelming the prompt
# Docs: https://python.langchain.com/docs/concepts/retrievers/
# || End of Initialization ||


# || Start of LLM Setup ||
model = OllamaLLM(model="llama3.2")
# Loads llama3.2 through Ollama as the LLM
# OllamaLLM is LangChain's wrapper around the Ollama library
# Runs completely locally — no API keys, no internet required
# Docs: https://python.langchain.com/docs/integrations/llms/ollama/

template = """You are CLEAR-AI, a waste disposal assistant for community and healthcare settings.

Use the following disposal guidelines from the knowledge base:
{context}

The following items have been detected: {items}

For each detected item provide:
1. Which bin it goes in (recycle, general waste, compost, hazardous, sharps)
2. Any preparation needed (rinse, flatten, remove lid, etc.)
3. Any specific warnings for community or healthcare settings

Be concise. One short paragraph per item. If the knowledge base does not contain
information about an item, use your general knowledge but flag it as general guidance."""
# The prompt template with two variables:
# {context} — relevant chunks retrieved from ChromaDB based on detected items
# {items}   — the detected item labels from YOLO
# The system role tells Ollama exactly what it is and how to respond
# Specific format requested — one paragraph per item keeps responses clean for Vue to display

prompt = ChatPromptTemplate.from_template(template)
# from_template() creates a reusable prompt object from the template string
# The {context} and {items} placeholders get filled in at runtime
# Docs: https://python.langchain.com/docs/concepts/prompt_templates/

chain = prompt | model
# The pipe operator | chains prompt and model together
# This is LangChain's LCEL (LangChain Expression Language) syntax
# When chain.invoke() is called:
# 1. prompt fills in {context} and {items} with real values
# 2. Passes the filled prompt to model (Ollama)
# 3. Ollama returns the disposal instructions
# Docs: https://python.langchain.com/docs/concepts/lcel/
# || End of LLM Setup ||


# || Start of Main Function ||
def get_disposal_instructions(detections: list) -> str:
    # Main function called by main.py after YOLO detects objects
    # Takes the detections list from detector.py
    # Returns disposal instructions as a string

    if not detections:
        return "No items detected."
    # Guard clause — if YOLO found nothing, return early
    # No point searching ChromaDB or calling Ollama with an empty list

    items = [d["label"] for d in detections]
    # List comprehension — loops through detections and pulls out just the label
    # detections = [{"label": "plastic bottle", "confidence": 0.94, "box": [...]}]
    # items = ["plastic bottle"]

    items_text = ", ".join(items)
    # Joins the list into a comma separated string
    # ["plastic bottle", "can"] → "plastic bottle, can"
    # This is what gets passed to ChromaDB search and into the prompt

    print(f"Getting disposal instructions for: {items_text}")

    relevant_docs = retriever.invoke(items_text)
    # Searches ChromaDB for the 3 most relevant chunks from your knowledge base
    # Uses semantic search — finds chunks with similar meaning to "plastic bottle, can"
    # Not just keyword matching — understands context and meaning
    # Returns a list of 3 document objects

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    # List comprehension pulls the text content from each retrieved document
    # "\n\n".join() joins them with two newlines between each chunk
    # This becomes the {context} variable in the prompt
    # Ollama reads this context before generating disposal instructions

    response = chain.invoke({
        "context": context,
        "items": items_text
    })
    # chain.invoke() fills in the prompt template and runs Ollama
    # "context" fills {context} in the template
    # "items" fills {items} in the template
    # Returns the full disposal instructions as a string
    # Docs: https://python.langchain.com/docs/concepts/lcel/

    return response
    # Returns the disposal instructions string back to main.py
    # main.py sends it to Vue as part of the JSON response
# || End of Main Function ||
=======
# Splits largs docs into smaller chunks to be processed by the LLM
# Docs: https://python.langchain.com/docs/how_to/recursive_text_splitter/

from langchain_chroma import Chroma
# Vector Sotre - stores documents and chunks as vectors
# Docs: https://python.langchain.com/docs/integrations/vectorstores/chroma/

from langchain_ollama import OllamaEmbeddings, OllamaLLM
# OllamaEmbeddings -> Convers chunks into vectors locally using llama3.2
>>>>>>> refs/remotes/origin/main
