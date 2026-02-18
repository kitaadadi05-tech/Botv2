import json, os, time, random
from config import STATS_FILE, ANALYTICS_FILE, BANNED_WORDS

# JSON safe load/save
def load_json(path, default):
    if os.path.exists(path):
        with open(path,"r") as f: return json.load(f)
    return default

def save_json(path, data):
    with open(path,"w") as f: json.dump(data,f)

# Daily stats
def update_stats(success=True):
    stats = load_json(STATS_FILE, {"today_uploads":0,"success":0,"failed":0,"last_reset":time.time()})
    if time.time()-stats["last_reset"]>86400:
        stats = {"today_uploads":0,"success":0,"failed":0,"last_reset":time.time()}
    stats["today_uploads"] += 1
    if success: stats["success"]+=1
    else: stats["failed"]+=1
    save_json(STATS_FILE, stats)

# Monetization safety
def monetization_safe(text):
    return not any(w in text.lower() for w in BANNED_WORDS)

def monetization_risk_score(text):
    score = sum(15 for w in BANNED_WORDS if w in text.lower())
    return min(score,100)

# Shadowban
def detect_shadowban():
    analytics = load_json(ANALYTICS_FILE, [])
    if not analytics: return False
    last_day = analytics[-1]
    try:
        views = float(last_day[0])
        impressions = float(last_day[3])
        if impressions>0 and views<impressions*0.005: return True
    except: return False
    return False

# Trend score
def trend_score(title):
    trend_words = ["2026","viral","ai","secret","new","trend"]
    score = sum(5 for w in trend_words if w in title.lower())
    score += random.randint(1,5)
    return score
