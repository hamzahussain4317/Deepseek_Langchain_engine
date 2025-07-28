from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_community.retrievers import BM25Retriever
# from fuzzy_search import extract_regulation_number , convert_num_words_to_digits
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


    
# def search_chroma(query):
#     vectordb=initialize_chroma()
#     #preprocessing
#     query=convert_num_words_to_digits(query)
#     lowered=query.lower()
#     is_comparison = any(x in lowered for x in ["compare", "difference", "differentiate", "versus", "vs", "between" , "comparison"])
    
#     matches = re.findall(r"regulation\s*[-–]?\s*(\d+)", query, re.IGNORECASE)
#     if is_comparison or len(matches) < 2:
#         fuzzy_matches = extract_regulation_number(query)
#         print("Fuzzy fallback matches: ", fuzzy_matches)
#         matches = list(set(matches + fuzzy_matches))  # merge unique
#     if matches:
#         # If multiple regulations are mentioned, retrieve chunks for all of them
#         results = []
#         for reg_number in matches:
#             docs = vectordb.similarity_search(query, k=3, filter={"regulation_number": reg_number})
#             results.extend(docs)
#         # Deduplicate by page content
#         return list({d.page_content: d for d in results}.values())
    
#     # Comparison without explicit regulation match – get general docs
#     if is_comparison:
#         return vectordb.similarity_search(query, k=5)
#     #hybrid searching BM25
#     if bm25_retriever:
#         bm25_docs=bm25_retriever.get_relevant_documents(query)
#         vector_docs=vectordb.similarity_search(query,k=3)
        
#         all_docs={d.page_content: d for d in (bm25_docs + vector_docs)}
#         return list(all_docs.values())[:5]
    
#     return vectordb.similarity_search(query,k=3)

def clear_chroma():
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)    