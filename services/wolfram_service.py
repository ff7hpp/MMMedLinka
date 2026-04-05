import os
import httpx
import xml.etree.ElementTree as ET

WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
WOLFRAM_URL = "http://api.wolframalpha.com/v2/query"

async def fetch_wolfram_data(query: str) -> str:
    # Use WolframAlpha API to retrieve specific medical facts
    params = {
        "input": query,
        "appid": WOLFRAM_APP_ID,
        "format": "plaintext"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(WOLFRAM_URL, params=params)
        if response.status_code != 200:
            return ""
        
        # Parse XML to extract plaintext
        try:
            root = ET.fromstring(response.text)
            result_texts = []
            for pod in root.findall('.//pod'):
                title = pod.get('title')
                for pt in pod.findall('.//plaintext'):
                    if pt.text:
                        result_texts.append(f"{title}: {pt.text}")
            return "\n".join(result_texts)
        except Exception:
            return ""
