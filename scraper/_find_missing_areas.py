"""Hittar omraden i CSV som saknas i coordinates.js."""
import csv
import re
from collections import Counter

CSV = r"D:\SwedishGeoHistori\SwedishGeoHistory\scraper\krig_events_enriched.csv"
COORDS = r"D:\SwedishGeoHistori\SwedishGeoHistory\frontend\src\utils\coordinates.js"


def main():
    with open(COORDS, encoding="utf-8") as f:
        text = f.read()
    existing = set(m.group(1) for m in re.finditer(r"'([^']+)':\s*\{\s*lat", text))
    print(f"Finns i coordinates.js: {len(existing)} nycklar")

    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    missing = Counter()
    for r in rows:
        a = r["area"].strip()
        if not a:
            continue
        if a.lower() not in existing:
            missing[a] += 1

    print(f"Saknas i coordinates.js: {len(missing)} unika areor ({sum(missing.values())} rader)")
    print()
    for a, c in missing.most_common(60):
        print(f"{c:4d}  {a}")


if __name__ == "__main__":
    main()
