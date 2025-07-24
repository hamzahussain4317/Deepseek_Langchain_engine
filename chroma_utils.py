from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import os,shutil,re
from fuzzywordsdetection import extract_regulation_number 

embeddings=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
persist_dir="./chroma_db"

def initialize_chroma():
    return Chroma(persist_directory=persist_dir ,embedding_function=embeddings)

def add_docs_to_chroma(docs:list[Document]):
    vectordb=initialize_chroma()
    for doc in docs:
      print(doc.metadata)
    vectordb.add_documents(docs)
    # vectordb.persist()
    
def search_chroma(query):
    vectordb=initialize_chroma()
    matches = re.findall(r"regulation\s*[-–]?\s*(\d+)", query, re.IGNORECASE)
    
    if not matches:
        matches=extract_regulation_number(query)
        print("matches from fuzzy words: ",matches)
    if matches:
        # If multiple regulations are mentioned, retrieve chunks for all of them
        results = []
        for reg_number in matches:
            docs = vectordb.similarity_search(query, k=3, filter={"regulation_number": reg_number})
            results.extend(docs)
        return results
    else:
        # No specific regulation mentioned, do general search
        return vectordb.similarity_search(query, k=3)
    # return vectordb.similarity_search(query, k=2)

def clear_chroma():
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)    