import os
import asyncio
import google.generativeai as genai

SYSTEM_PROMPT = (
    "You are MedLinka's medical AI assistant. "
    "Provide helpful, safe, and accurate health information. "
    "Always recommend consulting a real doctor for serious concerns. "
    "Keep responses concise and easy to understand."
)

def _call_gemini(prompt: str) -> str:
    """Synchronous Gemini call — runs inside a thread via asyncio.to_thread."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {prompt}")
    return response.text

async def get_gemini_response(message: str, context: str = "") -> str:
    """Async wrapper — offloads the blocking Gemini call to a thread."""
    prompt = message
    if context:
        prompt = f"Context:\n{context}\n\nUser question: {message}"

    # Run the blocking SDK call in a thread pool to avoid blocking the event loop
    return await asyncio.to_thread(_call_gemini, prompt)
