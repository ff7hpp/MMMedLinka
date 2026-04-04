import os
import httpx

OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY")
OPENFDA_URL = "https://api.fda.gov/drug/label.json"

async def search_medicine(query: str):
    params = {
        "search": f"brand_name:{query}+generic_name:{query}",
        "limit": 10
    }
    if OPENFDA_API_KEY:
        params["api_key"] = OPENFDA_API_KEY

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENFDA_URL, params=params)
            if response.status_code != 200:
                return []
            
            data = response.json()
            results = data.get("results", [])
            formatted = []
            for r in results:
                formatted.append({
                    "brand_name": r.get("openfda", {}).get("brand_name", [""])[0],
                    "generic_name": r.get("openfda", {}).get("generic_name", [""])[0],
                    "purpose": r.get("purpose", [""])[0],
                    "warnings": r.get("warnings", [""])[0],
                    "dosage": r.get("dosage_and_administration", [""])[0],
                    "adverse_reactions": r.get("adverse_reactions", [""])[0]
                })
            return formatted
        except Exception:
            return []
