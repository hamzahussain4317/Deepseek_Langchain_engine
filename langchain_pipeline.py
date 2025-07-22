from chroma_utils import search_chroma
from llm_client import ask_deepseek

def ask_llm(query:str):
    relevant_docs = search_chroma(query)  # 👈 use utility function
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    print('Context is: ',context)
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}"
    answer = ask_deepseek(prompt)
    return {"result": answer}