import json
from llm_client import ask_deepseek

def parse_query_with_llm(user_query:str)->dict:
    prompt = f"""
You are a strict query parser.
Your job is to extract whether the user wants to:
- retrieve factual info from AML regulations,
- summarize them,
- compare two regulations.

❌ DO NOT treat jokes, poems, stories, or casual/funny prompts as valid queries.

Return ONLY a JSON object with the following fields:
- "intent": one of ["summarize", "compare", "retrieve", "unknown"]
- "regulation": list of regulation numbers (as strings, like "2", "5", etc.)


If the user asks for a **joke**, **poem**, or anything funny or not professional, mark intent as `"unknown"`.

Only extract regulation numbers (e.g., "regulation 2" or "regulation five"). 
Ignore names of institutions, such as "SBP", "State Bank", "Pakistan", etc.

Convert written numbers like "five" to "5".

Example:
User query: "compare regulation 2 and five"
Response:
{{ "intent": "compare", "regulation": ["2", "5"] }}

User query: "What does SBP say about dealing with high-risk customers?"
Response:
{{ "intent": "retrieve", "regulation": [] }}

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
            parsed["regulation"] = [
                r for r in parsed.get("regulation", []) if r.isdigit()
            ]
            return parsed
    except Exception as e:
        print("❌ JSON parsing error:", e)
        print("⚠️ Raw response:", response)
    return {"intent":"unknown","regulation":[]}
    