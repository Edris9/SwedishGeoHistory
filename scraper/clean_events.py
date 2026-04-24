"""
Rensar krig_events_enriched.csv:
- Tar bort rader med area = Sverige / Okand / tom
- Tar bort duplikater baserat pa description (samma text, flera ar)
- Skriver tillbaka till samma fil
- Skriver ut SQL-kommandon for att rensa samma data i Supabase
"""
import csv
from collections import Counter, defaultdict

SRC = r"D:\SwedishGeoHistori\SwedishGeoHistory\scraper\krig_events_enriched.csv"
BAD = {"sverige", "okand", "okand", "okand", ""}


def normalize(s: str) -> str:
    return (s or "").strip().lower()


def main():
    with open(SRC, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Laser in: {len(rows)} rader")

    rows = [r for r in rows if normalize(r["area"]) not in BAD and r["area"].strip()]
    print(f"Efter Sverige/Okand-filter: {len(rows)}")

    groups = defaultdict(list)
    for r in rows:
        key = r["description"].strip()[:400]
        groups[key].append(r)
    print(f"Unika beskrivningar: {len(groups)}")

    dedup = []
    for desc, grp in groups.items():
        if len(grp) == 1:
            dedup.append(grp[0])
            continue
        best = min(grp, key=lambda r: (int(r["year"]) if r["year"].lstrip("-").isdigit() else 99999))
        dedup.append(best)

    print(f"Efter dedup: {len(dedup)}")
    print(f"Antal borttagna dubbletter: {len(rows) - len(dedup)}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "title", "description", "area", "source_url"])
        w.writeheader()
        w.writerows(dedup)
    print(f"\nSparade till: {SRC}")

    print("\nTopp 20 areor efter rensning:")
    for a, c in Counter(r["area"] for r in dedup).most_common(20):
        print(f"  {a}: {c}")


if __name__ == "__main__":
    main()
