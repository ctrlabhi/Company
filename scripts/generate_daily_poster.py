#!/usr/bin/env python3
"""Generate a date-specific illustration for the IntelliCore daily greeting card."""
import base64
import datetime as dt
import json
import os
import pathlib
import urllib.request
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "images" / "daily-posters" / "daily-art.png"
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1.5")
if not API_KEY:
    raise SystemExit("Missing OPENAI_API_KEY secret. Add it in GitHub repository Actions secrets.")

now = dt.datetime.now(ZoneInfo("Asia/Kolkata"))
date_key = now.strftime("%m-%d")
date_label = now.strftime("%d %B %Y")
occasion = {
    "01-01": "New Year, fresh beginnings and hopeful innovation",
    "01-12": "National Youth Day, young minds and bold ideas",
    "01-26": "India's Republic Day, unity and progress",
    "03-08": "International Women's Day, leadership and equal opportunity",
    "03-14": "Pi Day, mathematics and discovery",
    "03-22": "World Water Day, protecting water through responsible innovation",
    "04-22": "Earth Day, sustainability and a greener future",
    "05-01": "Labour Day, teamwork and respect for every contribution",
    "05-11": "National Technology Day in India, science and innovation",
    "06-05": "World Environment Day, technology for a healthier planet",
    "08-15": "India's Independence Day, freedom, unity and progress",
    "09-05": "Teachers' Day in India, learning and mentorship",
    "10-02": "Gandhi Jayanti, truth, peace and purposeful action",
    "10-20": "Dussehra and Vijayadashami, truth triumphing over evil, courage and new beginnings",
    "10-31": "National Unity Day in India, solidarity and teamwork",
    "11-14": "Children's Day in India, curiosity and imagination",
    "12-25": "Christmas season, kindness, hope and meaningful connection",
}.get(date_key, "a daily motivational theme about curiosity, teamwork, responsible technology, learning, and building a better future")

prompt = f"""Create a premium, polished visual illustration for a modern Indian technology company website, IntelliCore Technologies. Date: {date_label}. Today's theme: {occasion}.

Create ONLY the artwork, no text, no letters, no numbers, no logos, no watermark, no UI, no borders. Make the visual clearly fit today's theme and feel custom-created for this date. Combine tasteful cinematic storytelling with sophisticated blue/cyan corporate technology accents and warm natural lighting where appropriate. High-end editorial illustration, clean composition, crisp detail, uplifting and professional, appropriate for a reputable technology company. Keep the central area reasonably uncluttered so website text can sit nearby. Landscape 3:2 composition."""

payload = {
    "model": MODEL,
    "prompt": prompt,
    "size": "1536x1024",
    "quality": "medium",
    "output_format": "png",
}
req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))
except Exception as exc:
    raise SystemExit(f"OpenAI image generation failed: {exc}") from exc

image_b64 = result.get("data", [{}])[0].get("b64_json")
if not image_b64:
    raise SystemExit("Image API response did not contain data[0].b64_json")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_bytes(base64.b64decode(image_b64))
print(f"Generated {OUTPUT.relative_to(ROOT)} for {date_label} ({occasion}).")
