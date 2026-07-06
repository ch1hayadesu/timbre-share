import urllib.request, json, time

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

# Submit TTS
s, d = api("POST", "/tts/synthesize", {
    "voice_id": 1,
    "text": "Hello World, this is a test.",
    "speed": 1.0,
    "volume": 80,
    "pitch": 0,
})
rid = d["data"]["record_id"]
print(f"Submitted: record_id={rid} status={d['data']['status']}")

# Wait for processing
print("Waiting 8s...")
time.sleep(8)

# Check result
s, d = api("GET", f"/tts/history?page=1&page_size=20")
print(f"\nAll recent records:")
for item in d["data"]["items"]:
    print(f"  ID={item['record_id']} status={item['status']} url={item['audio_url']}")
    if item["record_id"] == rid:
        if item["status"] == 1 and item["audio_url"]:
            print(f"  -> SUCCESS! URL={item['audio_url']}")
        elif item["status"] == -1:
            print(f"  -> FAILED: {item.get('error_message', 'unknown')}")
