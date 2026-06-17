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
