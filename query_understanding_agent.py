import json
from llm_client import ask_deepseek

def parse_query_with_llm(user_query:str)->dict:
    prompt = f"""
You are a strict query parser.

Return ONLY a JSON object with the following fields:
- "intent": one of ["summarize", "compare", "retrieve", "unknown"]
- "regulation": list of regulation numbers (as strings)

Convert written numbers like "five" to "5".

Example:
User query: "compare regulation 2 and five"
Response:
{{ "intent": "compare", "regulation": ["2", "5"] }}

Now parse:
User query: "{user_query}"
"""

    response=ask_deepseek(prompt)
    print("response: ",response)
    
    # Clean markdown code block if exists
    if response.startswith("```"):
        response = response.strip().strip("`").replace("json", "", 1).strip()
    try:
       parsed = json.loads(response.strip())
       if isinstance(parsed, dict) and 'intent' in parsed:
            return parsed
    except Exception as e:
        print("❌ JSON parsing error:", e)
        print("⚠️ Raw response:", response)
    return {"intent":"unknown","regulation":[]}
    