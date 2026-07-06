import wave, struct, math, os

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), '..', 'ai-backend', 'static', 'samples')
SAMPLE_RATE = 16000
DURATION = 3
AMPLITUDE = 16000

presets = [
    ('gentle_female.wav', 260, '温柔女声'),
    ('mature_male.wav',   140, '成熟男声'),
    ('sweet_child.wav',   320, '甜美童声'),
    ('magnetic_male.wav', 110, '磁性男声'),
    ('intellectual_female.wav', 230, '知性女声'),
    ('news_anchor.wav',   180, '新闻播报'),
    ('anime_boy.wav',     350, '动漫正太'),
    ('queen_female.wav',  200, '御姐音'),
]

os.makedirs(SAMPLE_DIR, exist_ok=True)

for fname, freq, label in presets:
    path = os.path.join(SAMPLE_DIR, fname)
    frames = int(SAMPLE_RATE * DURATION)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(frames):
            t = i / SAMPLE_RATE
            val = int(AMPLITUDE * math.sin(2 * math.pi * freq * t))
            wf.writeframes(struct.pack('<h', val))
    size = os.path.getsize(path)
    print(f'{fname:35s} freq={freq:3d}Hz  size={size/1024:6.1f}KB  <- {label}')
