goteborg-historia/
├── frontend/           # React + Globe.gl
│   ├── src/
│   │   ├── components/
│   │   │   ├── Globe.jsx         # 3D-jordglob (interaktiv med mus/finger)
│   │   │   ├── RoleSelector.jsx  # Lärare/Student val
│   │   │   ├── Timeline.jsx      # Tidsväljare 12000 f.Kr - 2025
│   │   │   ├── EventPopup.jsx    # Visar händelse + AI-röst
│   │   │   ├── IssueReport.jsx   # Lärare: rapportera fel (knapp syns bara för lärare)
│   │   │   └── LanguageSwitcher.jsx # 🇸🇪 🇬🇧 🇸🇦 🇮🇷 flaggor
│   │   ├── pages/
│   │   │   ├── StudentView.jsx   # Student-vy
│   │   │   └── TeacherPortal.jsx # Samma vy + "Rapportera fel"-knapp
│   │   ├── locales/
│   │   │   ├── sv.json           # Svenska
│   │   │   ├── en.json           # English
│   │   │   ├── ar.json           # العربية
│   │   │   └── fa.json           # فارسی
│   │   └── App.jsx
│   └── package.json
│
├── backend/            # Node.js + Express
│   ├── routes/
│   │   ├── users.js
│   │   ├── events.js
│   │   └── issues.js
│   ├── db.js
│   └── server.js
│
└── scraper/            # Python    
    ├── scrape_wikipedia.py
    └── requirements.txt
