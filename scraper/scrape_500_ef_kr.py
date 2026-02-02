"""
Svenska Krig Scraper - Händelser efter 500 e.Kr.
================================================

OBS: Detta script är designat för att köras lokalt på din egen dator.
Det kräver internetåtkomst till Wikipedia, SO-rummet, Populär Historia, etc.

Installation:
    pip install requests beautifulsoup4 pandas

Användning:
    python sverige_krig_scraper.py

Output:
    krig_events.csv - CSV-fil med alla hittade händelser
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from urllib.parse import quote

headers = {"User-Agent": "SverigeHistoria/1.0 (studentprojekt; kontakt@example.com)"}

events = []
seen = set()  # För att undvika dubletter

# Svenska städer och orter (bas-lista för matchning)
svenska_stader = [
    # Storstäder
    'Stockholm', 'Göteborg', 'Malmö', 'Uppsala', 'Linköping', 'Örebro',
    'Västerås', 'Helsingborg', 'Norrköping', 'Jönköping', 'Lund', 'Umeå',
    'Gävle', 'Borås', 'Eskilstuna', 'Södertälje', 'Karlstad', 'Växjö',
    'Halmstad', 'Sundsvall', 'Östersund', 'Trollhättan', 'Luleå', 'Borlänge',
    'Falun', 'Kalmar', 'Skövde', 'Karlskrona', 'Kristianstad', 'Skellefteå',
    
    # Historiskt viktiga orter
    'Visby', 'Sigtuna', 'Birka', 'Gamla Uppsala', 'Vadstena', 'Strängnäs',
    'Nyköping', 'Arboga', 'Enköping', 'Söderköping', 'Skanör', 'Falsterbo',
    'Lödöse', 'Kungälv', 'Marstrand', 'Bohus', 'Älvsborg', 'Varberg',
    'Falkenberg', 'Laholm', 'Ängelholm', 'Landskrona', 'Trelleborg', 'Ystad',
    'Simrishamn', 'Sölvesborg', 'Karlshamn', 'Ronneby', 'Vimmerby', 'Västervik',
    'Oskarshamn', 'Nybro', 'Eksjö', 'Vetlanda', 'Tranås', 'Motala', 'Mjölby',
    'Vadstena', 'Skänninge', 'Askersund', 'Mariestad', 'Lidköping', 'Vara',
    'Alingsås', 'Ulricehamn', 'Tidaholm', 'Falköping', 'Herrljunga',
    
    # Norrland
    'Härnösand', 'Örnsköldsvik', 'Sollefteå', 'Kramfors', 'Ånge', 'Timrå',
    'Hudiksvall', 'Söderhamn', 'Bollnäs', 'Ljusdal', 'Mora', 'Ludvika',
    'Avesta', 'Hedemora', 'Säter', 'Piteå', 'Boden', 'Kalix', 'Haparanda',
    'Kiruna', 'Gällivare', 'Jokkmokk', 'Arvidsjaur', 'Lycksele', 'Vilhelmina',
    'Storuman', 'Dorotea', 'Strömsund', 'Sveg', 'Funäsdalen',
    
    # Dalarna/Bergslagen
    'Rättvik', 'Leksand', 'Orsa', 'Älvdalen', 'Malung', 'Vansbro', 'Gagnef',
    'Sälen', 'Idre', 'Filipstad', 'Hagfors', 'Torsby', 'Sunne', 'Arvika',
    'Åmål', 'Bengtsfors', 'Dals-Ed', 'Mellerud', 'Vänersborg', 'Uddevalla',
    'Lysekil', 'Strömstad', 'Tanum', 'Munkedal', 'Sotenäs', 'Orust',
    
    # Slag- och krigsplatser
    'Brunkeberg', 'Stångebro', 'Stäket', 'Brännkyrka', 'Gestilren', 'Lena',
    'Sparrsätra', 'Herrevadsbro', 'Ringsjö', 'Fotevik', 'Dünamünde',
    'Kirkholm', 'Kircholm', 'Kliszów', 'Fraustadt', 'Holowczyn',
    'Poltava', 'Fredrikshald', 'Narva', 'Nöteborg', 'Dorpat',
    'Riga', 'Reval', 'Stralsund', 'Wismar', 'Stettin', 'Wolgast',
    'Usedom', 'Rügen', 'Greifswald', 'Rostock', 'Lübeck', 'Bremen',
    'Verden', 'Stade', 'Hamburg', 'Breitenfeld', 'Lützen', 'Nördlingen',
    'Rain', 'Ingolstadt', 'München', 'Augsburg', 'Ulm', 'Mainz', 'Worms',
    'Frankfurt', 'Würzburg', 'Erfurt', 'Leipzig', 'Dresden', 'Prag',
    'Wien', 'Olmütz', 'Brünn', 'Jankow', 'Warschau', 'Krakow', 'Thorn',
    'Danzig', 'Elbing', 'Königsberg', 'Memel', 'Mitau', 'Dünaburg',
    
    # Landskap/regioner (som backup)
    'Skåne', 'Halland', 'Blekinge', 'Småland', 'Öland', 'Gotland',
    'Östergötland', 'Västergötland', 'Bohuslän', 'Dalsland', 'Värmland',
    'Närke', 'Södermanland', 'Uppland', 'Västmanland', 'Dalarna',
    'Gästrikland', 'Hälsingland', 'Medelpad', 'Ångermanland', 'Jämtland',
    'Härjedalen', 'Västerbotten', 'Norrbotten', 'Lappland'
]

def extract_location(text):
    """Extrahera plats/stad från texten."""
    # Först leta efter kända städer/platser
    for stad in svenska_stader:
        # Använd word boundary för att undvika delmatchningar
        pattern = r'\b' + re.escape(stad) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            return stad
    
    # Om ingen känd stad hittas, leta efter "i [Stad]" eller "vid [Stad]" mönster
    location_patterns = [
        r'i\s+([A-ZÅÄÖ][a-zåäö]+(?:\s+[A-ZÅÄÖ][a-zåäö]+)?)',
        r'vid\s+([A-ZÅÄÖ][a-zåäö]+(?:\s+[A-ZÅÄÖ][a-zåäö]+)?)',
        r'nära\s+([A-ZÅÄÖ][a-zåäö]+(?:\s+[A-ZÅÄÖ][a-zåäö]+)?)',
        r'utanför\s+([A-ZÅÄÖ][a-zåäö]+(?:\s+[A-ZÅÄÖ][a-zåäö]+)?)',
        r'mot\s+([A-ZÅÄÖ][a-zåäö]+(?:\s+[A-ZÅÄÖ][a-zåäö]+)?)',
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, text)
        if match:
            potential_location = match.group(1)
            # Filtrera bort vanliga ord som inte är platser
            skip_words = ['den', 'det', 'de', 'en', 'ett', 'och', 'eller', 'som', 'att', 'för', 'med', 'till', 'från', 'av', 'på', 'om', 'vid', 'efter', 'under', 'över', 'mellan', 'genom', 'utan', 'inom', 'enligt', 'mot', 'hos', 'än', 'så', 'hur', 'var', 'när', 'där', 'hit', 'dit', 'upp', 'ner', 'ut', 'in', 'hem', 'bort', 'fram', 'igen', 'också', 'bara', 'nog', 'ju', 'väl', 'nog', 'ändå', 'alltså', 'dock', 'alltid', 'aldrig', 'ofta', 'sällan', 'ibland', 'kanske', 'troligen', 'förmodligen', 'antagligen', 'säkert', 'verkligen', 'faktiskt', 'egentligen', 'ursprungligen', 'slutligen', 'tidigare', 'senare', 'sedan', 'redan', 'ännu', 'fortfarande', 'hittills', 'numera', 'nuförtiden', 'förr', 'förut', 'nyligen', 'snart', 'strax', 'genast', 'omedelbart', 'plötsligt', 'gradvis', 'successivt', 'långsamt', 'snabbt', 'hastigt']
            if potential_location.lower() not in skip_words and len(potential_location) > 2:
                return potential_location
    
    return "Okänd"

# Nyckelord för krig och konflikter
krig_keywords = [
    'krig', 'slag', 'strid', 'drabbning', 'konflikt', 'anfalla', 'anfall',
    'invasion', 'erövr', 'belägr', 'belägrade', 'armé', 'trupp', 'soldat',
    'viking', 'härtåg', 'plundra', 'brand', 'fälttåg', 'fred', 'fredsslut',
    'kapitulation', 'seger', 'nederlag', 'stupade', 'döda', 'offer',
    'vapen', 'svärd', 'kanon', 'flotta', 'sjöslag', 'landstigning',
    'försvar', 'befästning', 'borg', 'fästning', 'union', 'uppror',
    'revolt', 'mord', 'avrättning', 'blodba', 'massaker', 'härja',
    'belägrade', 'storm', 'erövrade', 'intog', 'förstörde', 'brände',
    'överfall', 'räd', 'plundr', 'brandskatt', 'gisslan', 'fångar'
]

def contains_war_keywords(text):
    """Kontrollera om texten innehåller krigsrelaterade nyckelord."""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in krig_keywords)

def extract_year(text):
    """Extrahera årtal från text (500-2000 e.Kr.)."""
    years = []
    
    # Leta efter explicita "e.Kr." först
    matches_ek = re.findall(r'(\d{3,4})\s*e\.?[Kk]r', text)
    for match in matches_ek:
        year = int(match)
        if 500 <= year <= 2000:
            years.append(year)
    
    # Leta efter vanliga årtal (1000-1999 antas vara e.Kr.)
    matches_year = re.findall(r'\b(1\d{3})\b', text)
    for match in matches_year:
        year = int(match)
        if year not in years and 500 <= year <= 2000:
            years.append(year)
    
    # Leta efter 500-999 om de nämns i historisk kontext
    matches_early = re.findall(r'\b([5-9]\d{2})\b', text)
    for match in matches_early:
        year = int(match)
        # Bara lägg till om texten verkar handla om historia
        if year not in years and 500 <= year <= 999:
            if any(word in text.lower() for word in ['viking', 'vendel', 'medeltid', 'århundrade', 'tal']):
                years.append(year)
    
    return list(set(years))  # Ta bort dubletter

def add_event(year, title, description, source_url):
    """Lägg till händelse om den inte redan finns."""
    if year < 500 or year > 2000:
        return False
    
    # Rensa beskrivningen
    description = ' '.join(description.split())  # Ta bort extra whitespace
    
    # Extrahera plats automatiskt från texten
    area = extract_location(description)
    
    # Unik nyckel: år + område + första 100 tecken av beskrivning
    key = f"{year}_{area}_{description[:100]}"
    
    if key in seen:
        return False
    seen.add(key)
    
    events.append({
        "year": year,
        "title": title,
        "description": description[:500].strip(),
        "area": area,
        "source_url": source_url
    })
    return True

def fetch_url(url, timeout=15):
    """Hämta URL med felhantering."""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Fel vid hämtning: {e}")
        return None

# ===================
# 1. WIKIPEDIA - KRIG OCH KONFLIKTER
# ===================
print("=" * 70)
print("1. WIKIPEDIA - KRIG OCH KONFLIKTER")
print("=" * 70)

wiki_krig_sidor = {
    # Övergripande militärhistoria
    "Sveriges_militärhistoria": "Sverige",
    "Lista_över_slag_i_Sverige": "Sverige",
    "Lista_över_krig_som_Sverige_deltagit_i": "Sverige",
    
    # Tidsåldrar
    "Vikingatiden": "Sverige",
    "Vendeltiden": "Sverige",
    "Sveriges_medeltid": "Sverige",
    "Kalmarunionen": "Sverige",
    "Stormaktstiden": "Sverige",
    "Svenska_frihetstiden": "Sverige",
    
    # Stora krig (kronologiskt)
    # Medeltida konflikter
    "Äldre_Vestgötalagens_krig": "Västergötland",
    "Slaget_vid_Fotevik": "Skåne",
    "Slaget_vid_Gestilren": "Sverige",
    "Slaget_vid_Lena": "Sverige",
    "Slaget_vid_Sparrsätra": "Sverige",
    "Folkungarnas_uppror": "Sverige",
    "Hatarnas_uppror": "Sverige",
    
    # Kalmarunionens konflikter
    "Engelbrektupproret": "Sverige",
    "Engelbrekt_Engelbrektsson": "Sverige",
    "Slaget_vid_Brunkeberg": "Sverige",
    "Stockholms_blodbad": "Sverige",
    "Daljunkern": "Dalarna",
    
    # Vasatiden
    "Gustav_Vasas_befrielsekrig": "Sverige",
    "Dackeupproret": "Småland",
    "Nils_Dacke": "Småland",
    "Nordiska_sjuårskriget": "Sverige",
    "Livländska_kriget": "Sverige",
    "Klubbekriget": "Sverige",
    
    # 1600-talets krig (Stormaktstiden)
    "Kalmarkriget": "Sverige",
    "De_la_Gardieska_fälttåget": "Sverige",
    "Polska_tronkrigen": "Sverige",
    "Trettioåriga_kriget": "Sverige",
    "Torstenssonskriget": "Sverige",
    "Karl_X_Gustavs_första_danska_krig": "Sverige",
    "Karl_X_Gustavs_andra_danska_krig": "Sverige",
    "Karl_X_Gustavs_krig_mot_Polen": "Sverige",
    "Karl_X_Gustavs_ryska_krig": "Sverige",
    "Skånska_kriget": "Skåne",
    "Snapphanekrigen": "Skåne",
    
    # 1700-talets krig
    "Stora_nordiska_kriget": "Sverige",
    "Pommerska_kriget": "Sverige",
    "Gustav_III:s_ryska_krig": "Sverige",
    "Teaterkriget": "Sverige",
    
    # 1800-talets krig
    "Finska_kriget": "Sverige",
    "Svensk-norska_kriget_1814": "Sverige",
    
    # Specifika slag
    "Slaget_vid_Brunkeberg": "Sverige",
    "Slaget_vid_Uppsala_1520": "Sverige",
    "Slaget_vid_Brännkyrka": "Sverige",
    "Slaget_vid_Stångebro": "Sverige",
    "Slaget_vid_Kirkholm": "Sverige",
    "Slaget_vid_Breitenfeld_(1631)": "Tyskland",
    "Slaget_vid_Lützen": "Tyskland",
    "Slaget_vid_Jankow": "Böhmen",
    "Slaget_vid_Warschau_(1656)": "Polen",
    "Slaget_vid_Lund": "Skåne",
    "Slaget_vid_Landskrona": "Skåne",
    "Slaget_vid_Narva": "Estland",
    "Slaget_vid_Kliszów": "Polen",
    "Slaget_vid_Poltava": "Ukraina",
    "Slaget_vid_Helsingborg_(1710)": "Skåne",
    "Slaget_vid_Gadebusch": "Tyskland",
    
    # Regionala historier med konflikter
    "Skånes_historia": "Skåne",
    "Gotlands_historia": "Gotland",
    "Bohusläns_historia": "Bohuslän",
    "Blekinges_historia": "Blekinge",
    "Hallands_historia": "Halland",
    "Jämtlands_historia": "Jämtland",
    
    # Vikingahändelser
    "Birka": "Sverige",
    "Ansgars_missioner": "Sverige",
    "Rurik": "Sverige",
    "Varangerna": "Sverige",
    "Ingvar_den_vittfarne": "Sverige",
    
    # Kungar och ledare (med krigshistoria)
    "Erik_Segersäll": "Sverige",
    "Olof_Skötkonung": "Sverige",
    "Anund_Jakob": "Sverige",
    "Erik_den_helige": "Sverige",
    "Birger_jarl": "Sverige",
    "Magnus_Ladulås": "Sverige",
    "Albrecht_av_Mecklenburg": "Sverige",
    "Karl_Knutsson_(Bonde)": "Sverige",
    "Kristian_II_av_Danmark": "Sverige",
    "Gustav_Vasa": "Sverige",
    "Erik_XIV": "Sverige",
    "Johan_III": "Sverige",
    "Karl_IX": "Sverige",
    "Gustav_II_Adolf": "Sverige",
    "Karl_X_Gustav": "Sverige",
    "Karl_XI": "Sverige",
    "Karl_XII": "Sverige",
    "Fredrik_I_av_Sverige": "Sverige",
    "Gustav_III": "Sverige",
    "Gustav_IV_Adolf": "Sverige",
}

for sida, region in wiki_krig_sidor.items():
    print(f"  Hämtar: {sida[:50]}...")
    
    url = "https://sv.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": sida,
        "format": "json",
        "prop": "text"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        if "error" in data:
            print(f"    ❌ Sidan finns inte")
            continue
        
        html = data["parse"]["text"]["*"]
        soup = BeautifulSoup(html, 'html.parser')
        
        # Ta bort referenser och fotnoter för renare text
        for ref in soup.find_all(['sup', 'span'], class_=['reference', 'mw-ref']):
            ref.decompose()
        
        count = 0
        for p in soup.find_all('p'):
            text = p.get_text()
            
            # Hoppa över korta stycken
            if len(text) < 50:
                continue
            
            # Kontrollera om texten innehåller krigsrelaterade ord
            if not contains_war_keywords(text):
                continue
            
            years = extract_year(text)
            
            for year in years:
                # Skapa en mer beskrivande titel
                title = f"Krig/konflikt i {region} {year}"
                if add_event(year, title, text, f"https://sv.wikipedia.org/wiki/{sida}"):
                    count += 1
        
        if count > 0:
            print(f"    ✅ {count} nya händelser")
        else:
            print(f"    ⚪ Inga nya händelser")
        
    except Exception as e:
        print(f"    ❌ Fel: {e}")
    
    time.sleep(0.3)  # Var snäll mot Wikipedia

# ===================
# 2. SO-RUMMET
# ===================
print("\n" + "=" * 70)
print("2. SO-RUMMET")
print("=" * 70)

so_sidor = [
    "https://www.so-rummet.se/fakta-artiklar/vikingatiden-i-sverige",
    "https://www.so-rummet.se/fakta-artiklar/vikingarnas-historia",
    "https://www.so-rummet.se/fakta-artiklar/vikingatidens-samhalle-och-kultur",
    "https://www.so-rummet.se/fakta-artiklar/sveriges-medeltid",
    "https://www.so-rummet.se/fakta-artiklar/kalmarunionen",
    "https://www.so-rummet.se/fakta-artiklar/stockholms-blodbad",
    "https://www.so-rummet.se/fakta-artiklar/gustav-vasa",
    "https://www.so-rummet.se/fakta-artiklar/vasatiden-i-sverige",
    "https://www.so-rummet.se/fakta-artiklar/stormaktstiden",
    "https://www.so-rummet.se/fakta-artiklar/den-svenska-stormaktstidens-uppgang",
    "https://www.so-rummet.se/fakta-artiklar/den-svenska-stormaktstidens-fall",
    "https://www.so-rummet.se/fakta-artiklar/trettioariga-kriget",
    "https://www.so-rummet.se/fakta-artiklar/trettioariga-krigets-orsaker-och-bakgrund",
    "https://www.so-rummet.se/fakta-artiklar/karl-xii",
    "https://www.so-rummet.se/fakta-artiklar/stora-nordiska-kriget",
    "https://www.so-rummet.se/fakta-artiklar/frihetstiden-1719-1772",
    "https://www.so-rummet.se/fakta-artiklar/gustavianska-tiden",
]

for url in so_sidor:
    filename = url.split('/')[-1][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('div', class_='article-content') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# 3. POPULÄR HISTORIA
# ===================
print("\n" + "=" * 70)
print("3. POPULÄR HISTORIA")
print("=" * 70)

ph_sidor = [
    "https://popularhistoria.se/sveriges-historia/vikingatiden",
    "https://popularhistoria.se/sveriges-historia/medeltiden",
    "https://popularhistoria.se/sveriges-historia/vasatiden",
    "https://popularhistoria.se/sveriges-historia/stormaktstiden",
    "https://popularhistoria.se/sveriges-historia/frihetstiden",
    "https://popularhistoria.se/krig-drabbningar",
    "https://popularhistoria.se/krig-drabbningar/trettioariga-kriget",
    "https://popularhistoria.se/krig-drabbningar/slaget-vid-lund-1676",
    "https://popularhistoria.se/krig-drabbningar/slaget-vid-poltava",
    "https://popularhistoria.se/sveriges-historia/stormaktstiden/karl-xii",
    "https://popularhistoria.se/sveriges-historia/medeltiden/stockholms-blodbad",
    "https://popularhistoria.se/sveriges-historia/vikingatiden/vikingarna",
    "https://popularhistoria.se/sveriges-historia/stormaktstiden/gustav-ii-adolf",
]

for url in ph_sidor:
    filename = url.split('/')[-1][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# 4. HISTORISKA MUSEET
# ===================
print("\n" + "=" * 70)
print("4. HISTORISKA MUSEET")
print("=" * 70)

hm_sidor = [
    "https://historiska.se/utforska-historien/tidsaldrar/vikingatiden/",
    "https://historiska.se/utforska-historien/tidsaldrar/medeltiden/",
    "https://historiska.se/utforska-historien/kunskapsbank/vikingar/",
    "https://historiska.se/utforska-historien/kunskapsbank/vikingatidens-vapen/",
]

for url in hm_sidor:
    filename = url.split('/')[-2][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# 5. KUNGAHUSET
# ===================
print("\n" + "=" * 70)
print("5. KUNGAHUSET")
print("=" * 70)

kh_sidor = [
    "https://www.kungahuset.se/monarkin/kungarochregenter",
    "https://www.kungahuset.se/monarkin/monarkinisverige",
]

for url in kh_sidor:
    filename = url.split('/')[-1][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# 6. RIKSARKIVET
# ===================
print("\n" + "=" * 70)
print("6. RIKSARKIVET")
print("=" * 70)

ra_sidor = [
    "https://riksarkivet.se/krig",
    "https://riksarkivet.se/militaria",
    "https://sok.riksarkivet.se/trettioariga-kriget",
]

for url in ra_sidor:
    filename = url.split('/')[-1][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# 7. LIVRUSTKAMMAREN
# ===================
print("\n" + "=" * 70)
print("7. LIVRUSTKAMMAREN")
print("=" * 70)

lrk_sidor = [
    "https://livrustkammaren.se/sv/historia/",
    "https://livrustkammaren.se/sv/samlingarna/vapen/",
]

for url in lrk_sidor:
    filename = url.split('/')[-2][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# 8. ARMÉMUSEUM
# ===================
print("\n" + "=" * 70)
print("8. ARMÉMUSEUM")
print("=" * 70)

am_sidor = [
    "https://www.armemuseum.se/utforska/tidslinjen/",
    "https://www.armemuseum.se/utforska/artiklar/",
]

for url in am_sidor:
    filename = url.split('/')[-2][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# 9. SVENSKT MILITÄRHISTORISKT BIBLIOTEK
# ===================
print("\n" + "=" * 70)
print("9. SVENSKT MILITÄRHISTORISKT BIBLIOTEK (SMHB)")
print("=" * 70)

smhb_sidor = [
    "https://www.militarhistoria.se/artiklar/",
]

for url in smhb_sidor:
    filename = url.split('/')[-2][:40]
    print(f"  Hämtar: {filename}...")
    
    response = fetch_url(url)
    if not response:
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    
    count = 0
    for p in article.find_all('p'):
        text = p.get_text()
        
        if len(text) < 50:
            continue
        
        if not contains_war_keywords(text):
            continue
        
        years = extract_year(text)
        
        for year in years:
            if add_event(year, f"Krig/konflikt {year}", text, url):
                count += 1
    
    if count > 0:
        print(f"    ✅ {count} nya händelser")
    else:
        print(f"    ⚪ Inga nya händelser")
    
    time.sleep(1)

# ===================
# SPARA RESULTAT
# ===================
print("\n" + "=" * 70)
print("RESULTAT")
print("=" * 70)

df = pd.DataFrame(events)

if len(df) > 0:
    df = df.sort_values("year")
    df = df.drop_duplicates(subset=["year", "area", "description"])
    
    # Spara till CSV
    df.to_csv("krig_events.csv", index=False, encoding="utf-8")
    
    print(f"\n✅ Totalt {len(df)} unika krigshändelser sparade till 'krig_events.csv'!")
    
    print(f"\n📍 FÖRDELNING PER OMRÅDE:")
    print("-" * 40)
    area_counts = df["area"].value_counts()
    for area, count in area_counts.items():
        print(f"  {area}: {count}")
    
    print(f"\n🔗 FÖRDELNING PER KÄLLA:")
    print("-" * 40)
    source_counts = df["source_url"].apply(lambda x: x.split("/")[2]).value_counts()
    for source, count in source_counts.items():
        print(f"  {source}: {count}")
    
    print(f"\n📝 EXEMPEL PÅ HÄNDELSER:")
    print("-" * 40)
    # Visa exempel från olika perioder
    sample_years = [600, 900, 1200, 1500, 1700]
    for target_year in sample_years:
        closest = df.iloc[(df['year'] - target_year).abs().argsort()[:1]]
        if not closest.empty:
            row = closest.iloc[0]
            print(f"\n  År {row['year']} ({row['area']}):")
            print(f"    {row['description'][:150]}...")
else:
    print("\n❌ Inga händelser hittades.")
    print("   Kontrollera att du har internetåtkomst till källorna.")
    print("   Scriptet är designat att köras lokalt på din dator.")