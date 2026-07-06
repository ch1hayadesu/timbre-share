import http.client
import json
import uuid
import time
import struct
import io

HOST = "127.0.0.1"
PORT = 8000

def encode_multipart(fields, files):
    """Build multipart/form-data body and return (body, boundary)."""
    boundary = uuid.uuid4().hex
    body = io.BytesIO()
    
    for name, value in fields:
        body.write(f"--{boundary}\r\n".encode())
        body.write(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.write(value.encode() if isinstance(value, str) else value)
        body.write(b"\r\n")
    
    for name, filename, data, content_type in files:
        body.write(f"--{boundary}\r\n".encode())
        body.write(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode())
        if content_type:
            body.write(f"Content-Type: {content_type}\r\n".encode())
        body.write(b"\r\n")
        body.write(data)
        body.write(b"\r\n")
    
    body.write(f"--{boundary}--\r\n".encode())
    return body.getvalue(), boundary

# Build minimal WAV
sample_rate = 16000
num_samples = 1600
data_size = num_samples * 2
wav_data = b"RIFF"
wav_data += struct.pack("<I", 36 + data_size)
wav_data += b"WAVE"
wav_data += b"fmt "
wav_data += struct.pack("<I", 16)
wav_data += struct.pack("<H", 1)
wav_data += struct.pack("<H", 1)
wav_data += struct.pack("<I", sample_rate)
wav_data += struct.pack("<I", sample_rate * 2)
wav_data += struct.pack("<H", 2)
wav_data += struct.pack("<H", 16)
wav_data += b"data"
wav_data += struct.pack("<I", data_size)
wav_data += bytes([0] * data_size)

body, boundary = encode_multipart(
    fields=[("voice_name", "Test Clone Voice"), ("clone_mode", "0")],
    files=[("file", "test.wav", wav_data, "audio/wav")],
)

# Send request
conn = http.client.HTTPConnection(HOST, PORT)
conn.request("POST", "/api/v1/voice/clone", body=body, headers={
    "Authorization": "Bearer 1",
    "Content-Type": f"multipart/form-data; boundary={boundary}",
})

resp = conn.getresponse()
print("Status:", resp.status)
data = json.loads(resp.read().decode())
print(json.dumps(data, indent=2, ensure_ascii=False))

if resp.status == 200 and data.get("data", {}).get("voice_id"):
    voice_id = data["data"]["voice_id"]
    print(f"\nVoice ID: {voice_id}")

    # Poll for completion
    print("\nPolling for status...")
    for i in range(10):
        time.sleep(3)
        conn2 = http.client.HTTPConnection(HOST, PORT)
        conn2.request("GET", f"/api/v1/voice/detail/{voice_id}", headers={"Authorization": "Bearer 1"})
        resp2 = conn2.getresponse()
        d2 = json.loads(resp2.read().decode())
        status = d2["data"]["status"]
        msg = d2["data"].get("error_message", "")
        print(f"  Poll {i+1}: status={status} msg={msg}")
        if status == 1:
            print("  -> Success! sample_url:", d2["data"].get("sample_url"))
            break
        elif status in (-1, 2):
            print("  -> Failed:", msg)
            break
    else:
        print("  -> Timeout")
else:
    print("Error:", data.get("message", "unknown"))

conn.close()
