import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def get_groq_response(message: str, context: str = ""):
    system_prompt = (
        "You are MedLinka's medical AI assistant. "
        "Provide helpful, safe, and accurate health information. "
        "Always recommend consulting a real doctor for serious concerns."
    )
    if context:
        system_prompt += f"\n\nHere is some factual context to consider: {context}"

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
