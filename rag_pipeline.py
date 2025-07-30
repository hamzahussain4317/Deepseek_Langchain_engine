from llm_client import ask_deepseek
from query_understanding_agent import parse_query_with_llm
from retriever_agent import retrieve_document
import json,re

last_llm_response=None
last_context=None
def extract_requirements():
    global last_llm_response
    global last_context
    print("last_llm_response: ", last_llm_response)
    if not last_llm_response:
        return{"error":"No previous LLM response found"}
    #mapped arrays
    mapped_frequency=["Monthly","Quaterly","Anually","Ongoing","Ad-hoc"]
    mapped_department=["Compliance", "Audit", "Risk", "IT", "HR", "Operations"]
    prompt = f"""
Assume the Role of a Compliance analyst at a bank. You will be given a circular by a regulator. 
Your task is to extract the requirements mentioned in the circular that the compliance department has to implement. 
Only pick the major requirements.

Select Frequency and Department from the following lists, if suitable:
- Frequency: {mapped_frequency}
- Department: {mapped_department}

Each requirement should include:
- Title (Same as Description, max 100 characters)
- Description (Extract the original text without any modification from the document or circular)
- Frequency
- Department
- RegulationNumber (Extract this from the circular’s Regulation number)

Always return response in JSON format:
{{
  "requirements": [
    {{
      "Title": "...",
      "Description": "...",
      "Frequency": "...",
      "Department": "...",
      "RegulationNumber": "..."
    }}
  ]
}}

Now extract from the following content:
{last_llm_response}
"""
    structured_response = ask_deepseek(prompt)
    print("structured_response: ", structured_response)
    if structured_response.startswith("```"):
       structured_response=structured_response.strip("`").replace("json","",1).strip()
    try:
        data=json.loads(structured_response)
        return{"response":data}
    except Exception as e:
        return {
            "error": "Failed to parse LLM response into JSON.",
            "raw": structured_response,
            "exception": str(e)
        }
def ask_llm(query:str):
    global last_llm_response
    global last_context
     # Step 1: Understand query intent
    parsed = parse_query_with_llm(query)
    print("Parsed Query:", parsed)
     # Step 2: Retrieve context
    docs,similarity_scores =retrieve_document(query,parsed)
    context = "\n\n".join([doc.page_content for doc in docs])
    last_context=context
    print("context: ",context)
    
    # Step 3: Early guard – if intent unknown or no docs found
    if parsed.get("intent") == "unknown" or similarity_scores < 0.65 or not context:
        return {
            "result": "❌ Sorry, your query does not match the context of the AML regulations. Please ask something related to anti-money laundering guidelines."
        }
    #sending extracted document and user query to LLM
    prompt = (
    f"Use the following context extracted from **AML Regulation** to answer the question accurately. "
    f"Always include a reference like 'According to AML Regulation' in your response.\n\n"
    f"{context}\n\n"
    f"Question: {query}"
)
    answer = ask_deepseek(prompt)
    last_llm_response=answer
    return {"result": answer}