# llm_client.py
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
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
