# MADE BY INC
# SUPPORTED LINK : https://discord.gg/ap4z3Mhy
#!/usr/bin/env python3
import time, os, re, requests, sys, itertools

# === CONFIG ===
SONG_NAME = "ONLY - Leehi"  
LYRIC_OFFSET = 0.0             
SIMULATED_LENGTH = 240         
SCROLL_SPEED = 0.05            
CREDITS = r"""
    \ INC /
     |____|
"""

# === COLOR HELPERS ===
def color(text, r, g, b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def fade_color(text, factor=0.5):
    r, g, b = (200, 200, 200)
    r, g, b = int(r * factor), int(g * factor), int(b * factor)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# === FETCH LYRICS ===
def fetch_lrc_from_lrclib(title: str, artist: str = "") -> str | None:
    try:
        res = requests.get(
            "https://lrclib.net/api/search",
            params={"q": f"{title} {artist}".strip()},
            timeout=10,
        )
        res.raise_for_status()
        for item in res.json():
            if item.get("syncedLyrics"):
                return item["syncedLyrics"]
    except Exception as e:
        print("⚠️  LRCLIB fetch failed:", e)
    return None

# === PARSE LRC ===
def parse_lrc_text(lrc_text: str):
    pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
    lines = []
    for line in lrc_text.splitlines():
        m = pattern.match(line.strip())
        if m:
            mins, secs, txt = m.groups()
            t = int(mins)*60 + float(secs) + LYRIC_OFFSET
            lines.append((max(0.0, t), txt.strip()))
    return sorted(lines)

# === MAIN ===
clear()
print(color(f"🎶 Fetching synced lyrics for: {SONG_NAME} ...", 255, 200, 50))
lrc_text = fetch_lrc_from_lrclib(SONG_NAME)
if not lrc_text:
    print(color("❌ No synced lyrics found online.", 255, 80, 80))
    sys.exit(1)

lyrics = parse_lrc_text(lrc_text)
print(color(f"✅ Found {len(lyrics)} lyric lines. Starting simulated playback...\n", 120, 255, 120))
time.sleep(1)

# === SIMULATED PLAYBACK ===
start_time = time.time()
lyric_index = 0
spinner = itertools.cycle(["\\", "|", "/"])
prev_lines = ["", ""]

while lyric_index < len(lyrics):
    elapsed = time.time() - start_time
    if elapsed >= lyrics[lyric_index][0]:
        clear()
        hue_step = int((time.time() * 5) % 360)
        r = int(127 + 127 * (1 + __import__('math').sin(hue_step / 30)))
        g = int(127 + 127 * (1 + __import__('math').sin((hue_step / 30) + 2)))
        b = int(127 + 127 * (1 + __import__('math').sin((hue_step / 30) + 4)))

        print(color(f"🎵 {SONG_NAME}", 255, 220, 150))
        print(color("-" * len(SONG_NAME), 120, 120, 120))
        print()

        if lyric_index > 0:
            print(fade_color(prev_lines[-1], 0.4))
        print(color(lyrics[lyric_index][1], r, g, b))
        print()

        prev_lines.append(lyrics[lyric_index][1])
        lyric_index += 1
    sys.stdout.write(color(f"   {next(spinner)} Playing... ", 100, 180, 255) + "\r")
    sys.stdout.flush()
    if elapsed > SIMULATED_LENGTH:
        break
    time.sleep(SCROLL_SPEED)

clear()
print(color("✅ Playback finished!", 100, 255, 100))
print(CREDITS)
print()
