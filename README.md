sverige-historia/
├── frontend/              # React + Globe.gl
│   ├── src/
│   │   ├── components/
│   │   │   ├── Globe.jsx
│   │   │   ├── RoleSelector.jsx
│   │   │   ├── Timeline.jsx
│   │   │   ├── EventPopup.jsx
│   │   │   ├── IssueReport.jsx
│   │   │   └── LanguageSwitcher.jsx
│   │   ├── pages/
│   │   │   ├── StudentView.jsx
│   │   │   └── TeacherPortal.jsx
│   │   ├── hooks/
│   │   │   ├── useLanguage.js
│   │   │   └── useEvents.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── locales/
│   │   │   ├── sv.json
│   │   │   ├── en.json
│   │   │   ├── ar.json
│   │   │   └── fa.json
│   │   └── App.jsx
│   └── package.json
│
├── backend-api/           # C# (.NET)
│   ├── Controllers/
│   │   ├── UsersController.cs
│   │   ├── EventsController.cs
│   │   └── IssuesController.cs
│   ├── Models/
│   │   ├── User.cs
│   │   ├── Event.cs
│   │   └── Issue.cs
│   ├── Data/
│   │   └── AppDbContext.cs
│   ├── Program.cs
│   └── appsettings.json
│
├── scraper/               # Python
│   ├── scrape_wikipedia.py
│   ├── db_connection.py
│   └── requirements.txt
│
├── .env.example           # Miljövariabler mall
└── README.md              # Projektdokumentation

## --------------------------------------------------------------------------------


# 🌍 Sverige Historia

En interaktiv webbapplikation som visualiserar Sveriges historia från stenåldern (12 000 f.Kr) till idag på en 3D-jordglob.

## 🎯 Vad är detta?

Användaren väljer om de är **lärare** eller **student**, sedan landar de på en interaktiv 3D-glob som visar Sverige. Genom att snurra globen (mus på dator, finger på mobil) och välja tidsperiod, visas historiska händelser som prickar på kartan.

Klicka på en prick → händelsen läses upp automatiskt med AI-röst.

## 👥 Användare

| Roll | Funktion |
|------|----------|
| Student | Utforska kartan, lyssna på händelser |
| Lärare | Samma som student + knapp för att rapportera fel |

## 🗣️ Språk

- 🇸🇪 Svenska
- 🇬🇧 English
- 🇸🇦 العربية
- 🇮🇷 فارسی

## ⏰ Tidsperiod

Från **12 000 f.Kr** (stenåldern – första människorna i Sverige) till **2025**.

## 🛠️ Tech Stack

| Del | Teknologi |
|-----|-----------|
| Frontend | React + Globe.gl |
| Backend | C# (.NET) |
| Databas | PostgreSQL | Supabase
| Scraper | Python |
| AI-röst | Web Speech API |
| Hosting | Railway + Netlify |

## 📁 Projektstruktur

```
sverige-historia/
├── frontend/           # React + Globe.gl
├── backend-api/        # C# (.NET)
├── scraper/            # Python
├── .env.example
└── README.md
```

## 🚀 Kom igång

*Kommer snart...*

## 📝 Felrapportering

Lärare kan rapportera felaktig information direkt i appen. Varje rapport får ett unikt ID och sparas i databasen för granskning.
