"""Kor klump-analys mot LIVE Supabase-data."""
import urllib.request
import json
import re
import sys
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding="utf-8")

COORDS = r"D:\SwedishGeoHistori\SwedishGeoHistory\frontend\src\utils\coordinates.js"
BASE = "https://wcasumuwrsusqqmgouze.supabase.co/rest/v1/events?select=area"
KEY = "sb_publishable_jTwXIQpfzIIyOOIKoOikBg_u8sEtVq8"

with open(COORDS, encoding="utf-8") as f:
    text = f.read()

pattern = re.compile(r"'([^']+)':\s*\{\s*lat:\s*(-?\d+\.?\d*),\s*lng:\s*(-?\d+\.?\d*)\s*\}")
coord_map = {m.group(1).lower(): (float(m.group(2)), float(m.group(3))) for m in pattern.finditer(text)}
print(f"coordinates.js: {len(coord_map)} nycklar")

alias_match = re.search(r"const\s+ALIASES\s*=\s*\{([^}]+)\}", text, re.DOTALL)
aliases = {}
if alias_match:
    for m in re.finditer(r"'([^']+)'\s*:\s*'([^']+)'", alias_match.group(1)):
        aliases[m.group(1).lower()] = m.group(2).lower()
print(f"aliaser: {len(aliases)}")

rows = []
page = 0
while True:
    s, e = page * 1000, page * 1000 + 999
    req = urllib.request.Request(
        BASE,
        headers={"apikey": KEY, "Authorization": f"Bearer {KEY}", "Range-Unit": "items", "Range": f"{s}-{e}"},
    )
    chunk = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
    if not chunk:
        break
    rows.extend(chunk)
    if len(chunk) < 1000:
        break
    page += 1
print(f"Hamtade {len(rows)} rader fran Supabase")

areas = Counter((r.get("area") or "").strip() for r in rows)

DEFAULT = (62.0, 17.0)
bucket = defaultdict(lambda: {"count": 0, "areas": []})
missing = []

for a, n in areas.items():
    key = a.lower()
    if key in aliases:
        key = aliases[key]
    coord = coord_map.get(key, DEFAULT)
    if coord == DEFAULT and key not in coord_map:
        missing.append((a, n))
    bucket[coord]["count"] += n
    bucket[coord]["areas"].append((a, n))

print("\n=== Topp 15 koordinat-klumpar ===")
for coord, info in sorted(bucket.items(), key=lambda x: -x[1]["count"])[:15]:
    marker = "  <-- DEFAULT (mitten av Sverige)" if coord == DEFAULT else ""
    print(f"{info['count']:5d}  ({coord[0]:6.2f}, {coord[1]:6.2f}){marker}")
    for a, n in sorted(info["areas"], key=lambda x: -x[1])[:5]:
        print(f"         {n:4d}  {a}")
    if len(info["areas"]) > 5:
        print(f"         ... + {len(info['areas']) - 5} fler")

print(f"\n=== {len(missing)} areor saknas i coordinates.js ({sum(n for _,n in missing)} rader) ===")
for a, n in sorted(missing, key=lambda x: -x[1])[:40]:
    print(f"{n:4d}  {a}")
