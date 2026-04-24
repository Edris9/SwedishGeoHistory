"""Hamtar live-data fran Supabase och raknar areor + mojibake."""
import urllib.request
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://wcasumuwrsusqqmgouze.supabase.co/rest/v1/events?select=area"
KEY = "sb_publishable_jTwXIQpfzIIyOOIKoOikBg_u8sEtVq8"

data = []
page = 0
while True:
    start = page * 1000
    end = start + 999
    req = urllib.request.Request(
        BASE,
        headers={
            "apikey": KEY,
            "Authorization": f"Bearer {KEY}",
            "Range-Unit": "items",
            "Range": f"{start}-{end}",
        },
    )
    chunk = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
    if not chunk:
        break
    data.extend(chunk)
    if len(chunk) < 1000:
        break
    page += 1

print(f"totalt rader hamtade: {len(data)}")

c = Counter((r.get("area") or "").strip() for r in data)
print("\ntopp 15 areor NU i Supabase:")
for a, n in c.most_common(15):
    print(f"  {n:4d}  \"{a}\"")

mb = [(a, n) for a, n in c.items() if "Ã" in a]
print(f"\nMojibake-rader kvar: {sum(n for _, n in mb)} (i {len(mb)} unika varden)")
for a, n in sorted(mb, key=lambda x: -x[1])[:10]:
    print(f"  {n:4d}  \"{a}\"")

okand = sum(n for a, n in c.items() if a.lower() in ("okänd", "sverige", ""))
print(f"\nSverige/Okand/tomma: {okand}")
