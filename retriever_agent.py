from chroma_utils import initialize_chroma , bm25_retriever
from langchain.schema import Document

def retrieve_document(user_query:str,parsed_query:dict)-> tuple[list[Document], float]:
    vectordb=initialize_chroma()
    regs=parsed_query.get("regulation",[])
    intent=parsed_query.get("intent",[])
    
    results_with_scores=vectordb.similarity_search_with_score(user_query,k=3)
    similarity_socres=results_with_scores[0][1] if results_with_scores else 0.0
    print("similarity scores: ",similarity_socres)
    
    if regs:
        results=[]
        for reg in regs:
            print("regulation no: ",reg)
            docs=vectordb.similarity_search(user_query,k=3,filter={"regulation_number":reg})
            results.extend(docs)
        print("extended document: ",docs)
        return list({d.page_content: d for d in results}.values()) ,  similarity_socres
        
        
    if bm25_retriever:
        bm25_docs=bm25_retriever.get_relevant_documents(user_query)
        vector_docs =vectordb.similarity_search(user_query,k=3)
        all_docs={d.page_content: d for d in (bm25_docs + vector_docs)}
        return list(all_docs.values())[:5] , similarity_socres
    
    
    return vectordb.similarity_search(user_query,k=3) , similarity_socres