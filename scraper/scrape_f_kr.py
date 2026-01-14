import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

headers = {"User-Agent": "SverigeHistoria/1.0 (studentprojekt)"}

events = []
seen = set()  # För att undvika dubletter

pattern = r'(\d{1,5})\s*(f\.Kr|f\.kr|fKr)'

def add_event(year, title, description, area, source_url):
    """Lägg till händelse om den inte redan finns."""
    # Unik nyckel: år + område + första 50 tecken av beskrivning
    key = f"{year}_{area}_{description[:50]}"
    
    if key in seen:
        return False
    seen.add(key)
    
    events.append({
        "year": year,
        "title": title,
        "description": description[:300].strip(),
        "area": area,
        "source_url": source_url
    })
    return True

# ===================
# 1. WIKIPEDIA
# ===================
print("=" * 50)
print("1. WIKIPEDIA")
print("=" * 50)

wiki_sidor = {
    "Sveriges_förhistoria": "Sverige",
    "Skånes_historia": "Skåne",
    "Gotlands_historia": "Gotland",
    "Upplands_historia": "Uppland",
    "Bohusläns_historia": "Bohuslän",
    "Västergötlands_historia": "Västergötland",
    "Östergötlands_historia": "Östergötland",
    "Smålands_historia": "Småland",
    "Norrlands_historia": "Norrland",
    "Dalarnas_historia": "Dalarna",
    "Värmlands_historia": "Värmland",
    "Blekinges_historia": "Blekinge",
    "Hallands_historia": "Halland"
}

for sida, region in wiki_sidor.items():
    print(f"  Hämtar: {sida}...")
    
    url = "https://sv.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": sida,
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "error" in data:
            print(f"    Sidan finns inte")
            continue
        
        html = data["parse"]["text"]["*"]
        soup = BeautifulSoup(html, 'html.parser')
        
        count = 0
        for p in soup.find_all('p'):
            text = p.get_text()
            matches = re.findall(pattern, text)
            
            for match in matches:
                year = -int(match[0])
                if add_event(year, f"Händelse {abs(year)} f.Kr", text, region, f"https://sv.wikipedia.org/wiki/{sida}"):
                    count += 1
        
        print(f"    ✅ {count} nya händelser")
        
    except Exception as e:
        print(f"    ❌ Fel: {e}")
    
    time.sleep(0.5)  # Var snäll mot servern

# ===================
# 2. SO-RUMMET
# ===================
print("\n" + "=" * 50)
print("2. SO-RUMMET")
print("=" * 50)

so_sidor = [
    ("https://www.so-rummet.se/fakta-artiklar/sverige-under-forntiden-del-1-stenaldern", "Sverige"),
    ("https://www.so-rummet.se/fakta-artiklar/sveriges-stenalder-bronsalder-och-jarnalder", "Sverige"),
]

for url, region in so_sidor:
    print(f"  Hämtar: {url[:50]}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"    ❌ Status: {response.status_code}")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Hitta artikelinnehåll
        article = soup.find('article') or soup.find('div', class_='article-content') or soup
        
        count = 0
        for p in article.find_all('p'):
            text = p.get_text()
            matches = re.findall(pattern, text)
            
            for match in matches:
                year = -int(match[0])
                if add_event(year, f"Händelse {abs(year)} f.Kr", text, region, url):
                    count += 1
        
        print(f"    ✅ {count} nya händelser")
        
    except Exception as e:
        print(f"    ❌ Fel: {e}")
    
    time.sleep(1)

# ===================
# 3. POPULÄR HISTORIA
# ===================
print("\n" + "=" * 50)
print("3. POPULÄR HISTORIA")
print("=" * 50)

ph_sidor = [
    ("https://popularhistoria.se/sveriges-historia/forntid/aldre-stenalder", "Sverige"),
    ("https://popularhistoria.se/sveriges-historia/forntid/yngre-stenalder-bonderna-ville-aga-sin-mark", "Sverige"),
]

for url, region in ph_sidor:
    print(f"  Hämtar: {url[:50]}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"    ❌ Status: {response.status_code}")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article = soup.find('article') or soup
        
        count = 0
        for p in article.find_all('p'):
            text = p.get_text()
            matches = re.findall(pattern, text)
            
            for match in matches:
                year = -int(match[0])
                if add_event(year, f"Händelse {abs(year)} f.Kr", text, region, url):
                    count += 1
        
        print(f"    ✅ {count} nya händelser")
        
    except Exception as e:
        print(f"    ❌ Fel: {e}")
    
    time.sleep(1)

# ===================
# 4. HISTORISKA MUSEET
# ===================
print("\n" + "=" * 50)
print("4. HISTORISKA MUSEET")
print("=" * 50)

hm_sidor = [
    ("https://historiska.se/utforska-historien/tidsaldrar/stenaldern-paleolitikum/", "Sverige"),
    ("https://historiska.se/utforska-historien/kunskapsbank/intro-till-stenaldern/", "Sverige"),
]

for url, region in hm_sidor:
    print(f"  Hämtar: {url[:50]}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"    ❌ Status: {response.status_code}")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article = soup.find('article') or soup.find('main') or soup
        
        count = 0
        for p in article.find_all('p'):
            text = p.get_text()
            matches = re.findall(pattern, text)
            
            for match in matches:
                year = -int(match[0])
                if add_event(year, f"Händelse {abs(year)} f.Kr", text, region, url):
                    count += 1
        
        print(f"    ✅ {count} nya händelser")
        
    except Exception as e:
        print(f"    ❌ Fel: {e}")
    
    time.sleep(1)

# ===================
# SPARA RESULTAT
# ===================
print("\n" + "=" * 50)
print("RESULTAT")
print("=" * 50)

df = pd.DataFrame(events)
df = df.sort_values("year")
df = df.drop_duplicates(subset=["year", "area", "description"])
df.to_csv("events.csv", index=False, encoding="utf-8")

print(f"\n✅ Totalt {len(df)} unika händelser sparade!")
print(f"\nFördelning per område:")
print(df["area"].value_counts())
print(f"\nFördelning per källa:")
print(df["source_url"].apply(lambda x: x.split("/")[2]).value_counts())