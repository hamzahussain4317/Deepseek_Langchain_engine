from chroma_utils import initialize_chroma , bm25_retriever
from langchain.schema import Document

def retrieve_document(user_query:str,parsed_query:dict)->list[Document]:
    vectordb=initialize_chroma()
    regs=parsed_query.get("regulations",[])
    intent=parsed_query.get("intent",[])
    
    if regs:
        results=[]
        for reg in regs:
            docs=vectordb.similarity_search(user_query,k=3,filter={"regulation_number":reg})
            results.extend(docs)
        return list({d.page_count: d for d in results}.values())
        
        
    if bm25_retriever:
        bm25_docs=bm25_retriever.get_relevant_documents(user_query)
        vector_docs =vectordb.similarity_search(user_query,k=3)
        all_docs={d.page_content: d for d in (bm25_docs + vector_docs)}
        return list(all_docs.values())[:5]
    
    
    return vectordb.similarity_search(user_query,k=3)