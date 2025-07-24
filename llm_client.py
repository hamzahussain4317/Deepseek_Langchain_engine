# llm_client.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def ask_deepseek(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[{"role": "user", "content": prompt}],
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "DeepSeekLangChainApp"
        }
    )
    return completion.choices[0].message.content
