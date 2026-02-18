import re, json, httpx, random
from config import OPENROUTER_API_KEY
from utils import monetization_safe, trend_score

async def generate_metadata(keyword):
    if not monetization_safe(keyword):
        keyword = "Amazing Viral Short"

    prompt = f"""
Generate:
- 5 viral YouTube Shorts titles
- 1 SEO description including #shorts
- 12 hashtags
Topic: {keyword}
Return JSON.
"""

    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type":"application/json"}
    payload = {"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":prompt}],"temperature":0.9}

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    content = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    content = re.sub(r"```json|```", "", content)
    data = {}
    try:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        data = json.loads(match.group()) if match else {}
        best_title = max(data.get("titles", ["Amazing Viral Short 2026"]), key=trend_score)
        description = data.get("description", "#shorts Viral Content 2026")
        hashtags = data.get("hashtags", ["shorts","viral","trend"])
    except:
        best_title, description, hashtags = "Amazing Viral Short 2026", "#shorts Viral Content", ["shorts","viral","trend"]

    return {"title": best_title[:90], "description": description, "hashtags": hashtags}
