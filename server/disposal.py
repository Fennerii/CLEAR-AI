# || Start of Imports ||
import os
# Python built in library, used to loop through files in the docs folder,
# build file paths, and check if the chroma_db folder already exists on disk.
# No installation needed.

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, BSHTMLLoader
# LangChain community loaders for each file type
# PyPDFLoader    -> reads PDF files
# Docx2txtLoader -> reads Word documents
# BSHTMLLoader   -> reads HTML files using BeautifulSoup
# Docs: https://python.langchain.com/docs/integrations/document_loaders/

from langchain_text_splitters import RecursiveCharacterTextSplitter
# Splits large documents into smaller chunks for vector storage.
# Moved to its own package in newer LangChain versions.
# Docs: https://python.langchain.com/docs/how_to/recursive_text_splitter/

from langchain_chroma import Chroma
# Vector store -- stores and searches document chunks as vectors
# Docs: https://python.langchain.com/docs/integrations/vectorstores/chroma/

from langchain_ollama import OllamaEmbeddings, OllamaLLM
# OllamaEmbeddings -> converts text chunks into vectors locally
#                     using a dedicated embeddings model
# OllamaLLM        -> runs the chat model locally for generating
#                     disposal instructions
# Docs: https://python.langchain.com/docs/integrations/llms/ollama/

from langchain_core.prompts import ChatPromptTemplate
# Builds reusable prompt templates with variables
# Docs: https://python.langchain.com/docs/concepts/prompt_templates/
# || End of Imports ||


# || Start of Paths ||
KNOWLEDGE_BASE_PATH = "docs"
# Folder containing the PDFs, DOCX and HTML files that make up the
# knowledge base. Path is relative to wherever uvicorn is run from.

CHROMA_DB_PATH = "chroma_db"
# Folder where the built vector store gets saved to disk.
# If this folder already exists, we load it directly instead of
# rebuilding everything from scratch -- this is what makes server
# restarts fast after the first successful build.
# || End of Paths ||


# || Start of Document Loading ||
def load_documents(folder: str) -> list:
    # Function that takes a folder path as a string.
    # Returns a flat list of all loaded document sections.
    # Only called when no existing vector store is found on disk.

    docs = []
    # Empty list that will be filled with loaded document sections.

    for filename in os.listdir(folder):
        # os.listdir returns every filename in the folder as a list.
        # We loop through each one to check its file type.

        filepath = os.path.join(folder, filename)
        # os.path.join builds the full file path.
        # folder = "docs"
        # filename = "recycling_rules.pdf"
        # filepath = "docs/recycling_rules.pdf"

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            # PyPDFLoader reads each page of the PDF as a separate document.

        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(filepath)
            # Docx2txtLoader extracts plain text from Word documents.

        elif filename.endswith(".html"):
            loader = BSHTMLLoader(filepath)
            # BSHTMLLoader uses BeautifulSoup to parse HTML.

        else:
            continue
            # Skip any file that is not PDF, DOCX or HTML.

        docs.extend(loader.load())
        # loader.load() returns a list of document objects.
        # extend() adds all of them to our docs list, flattening it.

    print(f"Loaded {len(docs)} document sections from {folder}")
    return docs
# || End of Document Loading ||


# || Start of Vector Store Builder ||
def build_vectorstore(docs: list, embeddings: OllamaEmbeddings) -> Chroma:
    # Takes the loaded documents and an embeddings model.
    # Splits, embeds, and saves everything to disk.
    # Returns a Chroma vectorstore object that can be searched immediately.

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    # Splits documents into chunks of 500 characters with 50 character
    # overlap so disposal instructions don't get cut off mid sentence.

    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    # from_documents converts every chunk into a vector using the
    # embeddings model, then saves everything into CHROMA_DB_PATH on disk.
    # persist_directory is what makes this reusable across restarts --
    # without it, everything would only live in memory and be lost
    # the moment the server stops.

    print("Vector store built and saved to disk")
    return vectorstore
# || End of Vector Store Builder ||


# || Start of Initialization ||
print("Loading knowledge base")

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
# Dedicated embeddings model. llama3.2 is a chat model and does not
# support the embeddings endpoint, which is why a separate model is
# required here specifically for converting text into vectors.

if os.path.exists(CHROMA_DB_PATH):
    # If the chroma_db folder already exists, the vector store was
    # already built in a previous run. Load it directly instead of
    # reprocessing every document and regenerating every embedding --
    # this is what makes subsequent server starts nearly instant.
    print("Existing vector store found, loading from disk")
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
else:
    # No existing vector store -- this is the first run, or chroma_db
    # was deleted. Load every document and build everything from scratch.
    print("No existing vector store found, building from scratch")
    docs = load_documents(KNOWLEDGE_BASE_PATH)
    vectorstore = build_vectorstore(docs, embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
# Converts the vectorstore into a retriever object.
# search_kwargs={"k": 3} means return the 3 most relevant chunks per search.
# Docs: https://python.langchain.com/docs/concepts/retrievers/
# || End of Initialization ||


# || Start of LLM Setup ||
model = OllamaLLM(model="llama3.2")
# Loads llama3.2 through Ollama as the chat model used to generate
# the actual disposal instructions. Runs completely locally.
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
# {context} -> relevant chunks retrieved from ChromaDB based on detected items
# {items}   -> the detected item labels from YOLO

prompt = ChatPromptTemplate.from_template(template)
# Builds a reusable prompt object with the two placeholders above.
# Docs: https://python.langchain.com/docs/concepts/prompt_templates/

chain = prompt | model
# Pipe operator chains the prompt and model together (LCEL syntax).
# chain.invoke() fills in the template, sends it to Ollama, and
# returns the generated disposal instructions.
# Docs: https://python.langchain.com/docs/concepts/lcel/
# || End of LLM Setup ||


# || Start of Main Function ||
def get_disposal_instructions(detections: list) -> str:
    # Main function called by main.py after YOLO detects objects.
    # Takes the detections list from detector.py.
    # Returns disposal instructions as a string.

    if not detections:
        return "No items detected."
    # Guard clause -- nothing to search or generate if YOLO found nothing.

    items = [d["label"] for d in detections]
    # Pulls just the label out of each detection dictionary.
    # detections = [{"label": "plastic bottle", "confidence": 0.94, "box": [...]}]
    # items = ["plastic bottle"]

    items_text = ", ".join(items)
    # Joins the list into a comma separated string for the search query
    # and the prompt. ["plastic bottle", "can"] -> "plastic bottle, can"

    print(f"Getting disposal instructions for: {items_text}")

    relevant_docs = retriever.invoke(items_text)
    # Searches ChromaDB for the 3 most relevant chunks using semantic
    # search -- matches by meaning, not just exact keywords.

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    # Joins the retrieved chunks into a single context string that
    # gets passed into the prompt template.

    response = chain.invoke({
        "context": context,
        "items": items_text
    })
    # Fills in the prompt template and runs it through Ollama.
    # Returns the full disposal instructions as a string.

    return response
# || End of Main Function ||