# Polski Fach - Marketplace Platform

Platforma marketplace dla polskich fachowców - łącząca klientów z wykonawcami usług.

## 🏗️ Architektura

- **Backend**: Django REST Framework (Python)
- **Frontend**: Next.js 15 + React 19 (TypeScript)
- **Baza danych**: PostgreSQL (Neon)
- **Deployment**: 
  - Backend: Fly.io
  - Frontend: Vercel

## 🚀 Quick Start

### Backend (Django)

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (Next.js)

```bash
cd web
npm install
npm run dev
```

## 📁 Struktura projektu

```
polskifachv2/
├── server/                 # Django backend
│   ├── core/              # Django settings
│   ├── marketplace/       # Główna aplikacja
│   ├── Dockerfile         # Container dla Fly.io
│   ├── fly.toml          # Konfiguracja Fly.io
│   └── requirements.txt   # Python dependencies
├── web/                   # Next.js frontend
│   ├── src/
│   │   ├── app/          # App Router (Next.js 13+)
│   │   ├── hooks/        # Custom React hooks
│   │   └── lib/          # Utilities i API client
│   ├── package.json      # Node.js dependencies
│   └── vercel.json       # Konfiguracja Vercel
└── README.md
```

## 🔧 Konfiguracja

### Zmienne środowiskowe - Backend

```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=your-app.fly.dev
```

### Zmienne środowiskowe - Frontend

```bash
NEXT_PUBLIC_API_URL=https://your-backend.fly.dev
```

## 🚀 Deployment

### Backend na Fly.io

```bash
cd server
fly auth login
fly apps create your-app-name
fly secrets set SECRET_KEY="your-key"
fly secrets set DATABASE_URL="your-db-url"
fly deploy
```

### Frontend na Vercel

1. Importuj folder `web` na Vercel
2. Ustaw `NEXT_PUBLIC_API_URL`
3. Deploy!

## 📋 Funkcjonalności

- ✅ Rejestracja i logowanie użytkowników
- ✅ Profil wykonawcy/usługodawcy
- ✅ Katalog usług i kategorii
- ✅ System wiadomości
- ✅ Recenzje i oceny
- ✅ Panel administracyjny

## 🛠️ Tech Stack

**Backend:**
- Django 5.x
- Django REST Framework
- JWT Authentication
- PostgreSQL
- CORS Headers

**Frontend:**
- Next.js 15
- React 19
- TypeScript
- Axios
- Tailwind CSS (planowane)

## 📝 Licencja

MIT License
