from llm_client import ask_deepseek
from query_understanding_agent import parse_query_with_llm
from retriever_agent import retrieve_document


def ask_llm(query:str):
    #retrieve document from chroma
    parsed = parse_query_with_llm(query)
    print("Parsed Query:", parsed)
    docs=retrieve_document(query,parsed)
    context = "\n\n".join([doc.page_content for doc in docs])
    print("context: ",context)
    #sending extracted document and user query to LLM
    prompt = (
    f"Use the following context extracted from **AML Regulation** to answer the question accurately. "
    f"Always include a reference like 'According to AML Regulation' in your response.\n\n"
    f"{context}\n\n"
    f"Question: {query}"
)
    answer = ask_deepseek(prompt)
    return {"result": answer}