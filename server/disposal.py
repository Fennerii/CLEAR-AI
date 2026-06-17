# || Start of Imports ||
import os
#Built in library in python, used to loop through files in our knowledge base folder
#Builds file paths

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, BSHTMLLoader
# Langchain community loaders for each given file type
# PyPDFLoader -> Reads PDF Files
# Docx2txtLoader -> Reads Words Documents
# BSTMLLoader -> Reads HTML Files using BeautifulSoup
#Docs: https://python.langchain.com/docs/integrations/document_loaders/

from langchain.text_splitter import RecursiveCharacterTextSplitter
# Splits largs docs into smaller chunks to be processed by the LLM
# Docs: https://python.langchain.com/docs/how_to/recursive_text_splitter/

from langchain_chroma import Chroma
# Vector Sotre - stores documents and chunks as vectors
# Docs: https://python.langchain.com/docs/integrations/vectorstores/chroma/

from langchain_ollama import OllamaEmbeddings, OllamaLLM
# OllamaEmbeddings -> Convers chunks into vectors locally using llama3.2