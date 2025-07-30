from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_community.retrievers import BM25Retriever
import os,shutil,re
 

embeddings=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
persist_dir="./chroma_db"
bm25_retriever=None

def initialize_chroma():
    return Chroma(persist_directory=persist_dir ,embedding_function=embeddings)

def add_docs_to_chroma(docs:list[Document]):
    vectordb=initialize_chroma()
    for doc in docs:
      print(doc.metadata)
    vectordb.add_documents(docs)

def setup_bm25_retriever(docs:list[Document]):
    global bm25_retriever
    bm25_retriever=BM25Retriever.from_documents(docs)
    bm25_retriever.k=3


    
def clear_chroma():
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)    