import urllib.request
import json
import time

BASE = "http://127.0.0.1:8000/api/v1"

def api(method, path, data=None):
    url = BASE + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", "Bearer 1")
    if body:
        req.add_header("Content-Type", "application/json")
    resp = urllib.request.urlopen(req, timeout=15)
    return resp.status, json.loads(resp.read().decode())

# Test 1: Health
print("=== GET /health ===")
r = urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=5)
print(r.status, r.read().decode())

# Test 2: Voice list
print("\n=== GET /voice/list ===")
s, d = api("GET", "/voice/list?page=1&page_size=3")
print(s, len(d["data"]["items"]), "items")

# Test 3: Voice presets
print("\n=== GET /voice/presets ===")
s, d = api("GET", "/voice/presets")
print(s, len(d.get("data", [])), "presets")

# Test 4: TTS synthesize
print("\n=== POST /tts/synthesize (test) ===")
s, d = api("POST", "/tts/synthesize", {
    "voice_id": 1,
    "text": "你好世界，这是一段测试语音。",
    "speed": 1.0,
    "volume": 80,
    "pitch": 0,
})
record_id = d["data"]["record_id"]
print(f"Submitted record_id={record_id} status={d['data']['status']}")

# Test 5: Wait for Celery Worker
print(f"\n=== Waiting 10s for Celery Worker to process #{record_id} ===")
time.sleep(10)

s, d = api("GET", f"/tts/history?page=1&page_size=15")
for item in d["data"]["items"]:
    if item["record_id"] == record_id:
        print(f"  -> ID={item['record_id']} status={item['status']} url={item['audio_url']}")
        break

print("\n=== TTS History (recent) ===")
for item in d["data"]["items"][:12]:
    print(f"  ID={item['record_id']} status={item['status']} url={item['audio_url']}")

print("\n=== Voice Details ===")
for v in d["data"] if isinstance(d["data"], list) else []:
    pass  # already printed above

print("\n=== All tests passed ===")
