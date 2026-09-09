#!/usr/bin/env python3
import re
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} input.srt shift-ms", file=sys.stderr)
    print("Example: shift_srt.py subtitles.srt 1500", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]
shift_ms = int(sys.argv[2])

timestamp = re.compile(
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})"
)

def adjust(match):
    h, m, s, ms = map(int, match.groups())
    total = ((h * 60 + m) * 60 + s) * 1000 + ms
    total = max(0, total + shift_ms)

    h, remainder = divmod(total, 3_600_000)
    m, remainder = divmod(remainder, 60_000)
    s, ms = divmod(remainder, 1_000)

    return f"{h:02}:{m:02}:{s:02},{ms:03}"

with open(input_file, encoding="utf-8-sig") as f:
    text = f.read()

text = timestamp.sub(adjust, text)

with open(input_file + ".fixed.srt", "w", encoding="utf-8", newline="") as f:
    f.write(text)

