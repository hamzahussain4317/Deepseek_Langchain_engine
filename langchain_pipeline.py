from chroma_utils import search_chroma
from llm_client import ask_deepseek

def ask_llm(query:str):
    relevant_docs = search_chroma(query)
    print("relevant docs: ",relevant_docs)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    print('Context is: ',context)
    prompt = (
    f"Use the following context extracted from **AML Regulation** to answer the question accurately. "
    f"Always include a reference like 'According to AML Regulation' in your response.\n\n"
    f"{context}\n\n"
    f"Question: {query}"
)
    answer = ask_deepseek(prompt)
    return {"result": answer}