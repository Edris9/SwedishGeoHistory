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
└── scraper/            # Python
    ├── scrape_wikipedia.py
    └── requirements.txt