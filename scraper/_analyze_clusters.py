"""Jamfor areor i Supabase mot coordinates.js och grupperar per koordinat."""
import json
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

DB = r"D:\SwedishGeoHistori\SwedishGeoHistory\scraper\_db_areas.json"
COORDS = r"D:\SwedishGeoHistori\SwedishGeoHistory\frontend\src\utils\coordinates.js"

with open(COORDS, encoding="utf-8") as f:
    text = f.read()

pattern = re.compile(r"'([^']+)':\s*\{\s*lat:\s*(-?\d+\.?\d*),\s*lng:\s*(-?\d+\.?\d*)\s*\}")
coord_map = {}
for m in pattern.finditer(text):
    key = m.group(1).lower()
    lat = float(m.group(2))
    lng = float(m.group(3))
    coord_map[key] = (lat, lng)
print(f"coordinates.js: {len(coord_map)} nycklar")
for probe in ("skåne", "jämtland", "malmö", "göteborg", "bohuslän"):
    print(f"  probe '{probe}': {'JA' if probe in coord_map else 'NEJ'}  coord={coord_map.get(probe)}")

alias_match = re.search(r"const\s+ALIASES\s*=\s*\{([^}]+)\}", text, re.DOTALL)
aliases = {}
if alias_match:
    for m in re.finditer(r"'([^']+)'\s*:\s*'([^']+)'", alias_match.group(1)):
        aliases[m.group(1).lower()] = m.group(2).lower()
print(f"aliaser: {len(aliases)}")

with open(DB, encoding="utf-8-sig") as f:
    areas = json.load(f)

DEFAULT = (62.0, 17.0)
bucket = defaultdict(lambda: {"count": 0, "areas": []})
missing = []
total = 0

for row in areas:
    a = (row["area"] or "").strip()
    n = row["antal"]
    total += n
    key = a.lower()
    if key in aliases:
        key = aliases[key]
    if key in coord_map:
        coord = coord_map[key]
    else:
        coord = DEFAULT
        missing.append((a, n))
    bucket[coord]["count"] += n
    bucket[coord]["areas"].append((a, n))

print(f"Totalt rader: {total}")
print()
print("=== Topp 20 KOORDINAT-klumpar (flest prickar pa samma punkt) ===")
for coord, info in sorted(bucket.items(), key=lambda x: -x[1]["count"])[:20]:
    marker = " <-- DEFAULT (mitten av Sverige)" if coord == DEFAULT else ""
    print(f"{info['count']:5d}  ({coord[0]:6.2f}, {coord[1]:6.2f}){marker}")
    for a, n in sorted(info["areas"], key=lambda x: -x[1])[:5]:
        print(f"         {n:4d}  {a}")
    if len(info["areas"]) > 5:
        print(f"         ... + {len(info['areas']) - 5} fler")

print()
print(f"=== Areor som saknas i coordinates.js: {len(missing)} unika, {sum(n for _,n in missing)} rader ===")
for a, n in sorted(missing, key=lambda x: -x[1])[:30]:
    print(f"{n:4d}  {a}")
