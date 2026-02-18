import os, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import TOKEN_FILE, SCOPES
from utils import trend_score

def get_youtube_service():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE,SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE,"w") as f: f.write(creds.to_json())
    return build("youtube","v3",credentials=creds)

def detect_category(keyword):
    keyword=keyword.lower()
    if any(x in keyword for x in ["game","minecraft","pubg"]): return "20"
    if any(x in keyword for x in ["tech","ai","robot"]): return "28"
    if any(x in keyword for x in ["learn","how","tutorial"]): return "27"
    return "24"

def predict_ctr(title):
    base_score = trend_score(title)
    return round(min(5 + base_score*0.3,25),2)

def title_performance_score(title):
    score = 10 if len(title)<60 else 0
    score += 15 if any(x in title.lower() for x in ["how","secret","ai","new"]) else 0
    score += trend_score(title)
    score += predict_ctr(title)
    return round(score,2)

def _upload_sync(path, metadata, progress_callback=None):
    youtube=get_youtube_service()
    body={"snippet":{"title":metadata.get("title","Viral Short 2026"),
                     "description":metadata.get("description","#shorts"),
                     "tags":metadata.get("hashtags",["shorts","viral"]),
                     "categoryId":metadata.get("category","22")},
          "status":{"privacyStatus":"public"}}
    media=MediaFileUpload(path,chunksize=1024*1024,resumable=True)
    request=youtube.videos().insert(part="snippet,status",body=body,media_body=media)
    response=None
    start_time=time.time()
    total=os.path.getsize(path)
    while response is None:
        status,response=request.next_chunk()
        if status and progress_callback:
            uploaded=status.resumable_progress
            percent=int(uploaded/total*100)
            speed=uploaded/(time.time()-start_time+0.1)
            eta=(total-uploaded)/(speed+1)
            progress_callback(percent,round(eta,1))
    return f"https://youtube.com/watch?v={response['id']}"

async def upload_video(path, metadata, progress_message):
    import asyncio
    loop=asyncio.get_running_loop()
    def progress_callback(percent, eta):
        asyncio.run_coroutine_threadsafe(
            progress_message.edit_text(f"🚀 Uploading...\nProgress: {percent}%\nETA: {eta}s"), loop
        )
    return await loop.run_in_executor(None,_upload_sync,path,metadata,progress_callback)
