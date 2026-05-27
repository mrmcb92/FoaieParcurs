# TripLog 🚗

**Calcul automat km pentru foaia de parcurs**

[🇬🇧 English](#-english)

🔗 **Aplicație live**: [triplog-05n6.onrender.com](https://triplog-05n6.onrender.com)

> ⚠️ La prima accesare după o perioadă de inactivitate, aplicația poate dura 30–50 de secunde să pornească (limitare a planului gratuit Render).

---

## ✨ Funcționalități

- Autocomplete pentru adrese cu sugestii din OpenStreetMap
- Calcul automat al distanțelor prin OSRM
- Toggle „dus-întors" și multiplicator (×) pe fiecare segment
- Închidere circuit — revenire la punctul de plecare
- Reordonare opriri prin drag-and-drop sau butoane sus/jos
- Buton „Locația mea" cu geocodare inversă
- **Hartă interactivă** Leaflet cu traseul calculat
- **Gestionare vehicule** — nume, nr. înmatriculare, consum, preț carburant, șofer
- **Calcul cost** per cursă în funcție de consumul vehiculului
- **Câmpuri odometru** km start / km final (stocate în istoric)
- **Scop cursă** per segment
- **Favorite** — salvare/încărcare trasee frecvente cu export/import JSON
- **Istoric curse** — toate traseele salvate, filtrare pe lună
- **Raport lunar Excel** direct din istoric
- **Partajare traseu** prin URL (link copiabil)
- **Buton Traseu nou** — resetare rapidă pentru o nouă cursă fără a reporni aplicația
- Export **Excel**, **CSV** și **PDF**
- Navigare în 5 tab-uri: Traseu · Hartă · Segmente · Export · Istoric
- Interfață mobile-first, dark/light mode, toggle limbă RO/EN
- **PWA** — instalabilă pe Android și iOS ca aplicație nativă

---

## 🛠️ Stack tehnic

| Component | Tehnologie |
|-----------|-----------|
| Backend | FastAPI (Python 3) + uvicorn |
| Frontend | React 18 (CDN, fără build step), Babel in-browser |
| Hartă | Leaflet.js 1.9 |
| Geocodare | LocationIQ → Nominatim → maps.co (fallback în cascadă) |
| Geocodare inversă | Nominatim `/reverse` |
| Rutare | OSRM (router.project-osrm.org) |
| Export Excel | pandas + openpyxl |
| Export PDF | reportlab |
| Cache server | SQLite via aiosqlite |
| Rate limiting | slowapi (60 req/min per IP) |
| Hosting | Render (plan gratuit) |

---

## 📁 Structura proiectului

```
triplog/
├── main.py              # Backend FastAPI
├── requirements.txt     # Dependențe Python
├── render.yaml          # Configurare deployment Render
├── README.md
└── static/
    ├── index.html       # Frontend React (single-file SPA)
    ├── manifest.json    # PWA manifest
    ├── sw.js            # Service worker
    ├── icon-192.png     # Iconiță PWA
    └── icon-512.png     # Iconiță PWA
```

---

## 🚀 Rulare locală

1. Clonează repo-ul:
   ```bash
   git clone https://github.com/mrmcb92/triplog.git
   cd triplog
   ```

2. Instalează dependențele:
   ```bash
   pip install -r requirements.txt
   ```

3. (Opțional) Setează variabilele de mediu:
   ```bash
   export LOCATIONIQ_KEY="cheia_ta_aici"
   export CONTACT_EMAIL="email@example.com"
   export ALLOWED_ORIGINS="https://domeniul-tau.com"
   ```
   Fără `LOCATIONIQ_KEY`, aplicația folosește Nominatim (gratuit, puțin mai lent).

4. Pornește serverul:
   ```bash
   uvicorn main:app --reload
   ```

5. Deschide [http://localhost:8000](http://localhost:8000) în browser.

---

## ☁️ Deployment pe Render

Repo-ul include `render.yaml`. Pași:

1. Creează un cont pe [render.com](https://render.com)
2. New → Web Service → conectează acest repo
3. Setările sunt detectate automat din `render.yaml`
4. (Opțional) Adaugă în Environment Variables:
   - `LOCATIONIQ_KEY` — cheie API LocationIQ pentru geocodare mai rapidă
   - `CONTACT_EMAIL` — email pentru header-ul User-Agent Nominatim
   - `ALLOWED_ORIGINS` — origini permise CORS (implicit `*`)

---

## 📱 Instalare PWA

**Android (Chrome):** Deschizi aplicația → meniu trei puncte → „Adaugă pe ecranul principal"

**iPhone (Safari):** Deschizi aplicația în Safari → butonul Share → „Adaugă pe ecranul principal"

Aplicația se deschide fullscreen, fără bara browserului, ca o aplicație nativă.

---

## 🔌 API endpoints

| Endpoint | Metodă | Descriere |
|----------|--------|-----------|
| `/api/geocode?q={query}&limit={n}` | GET | Caută adrese, returnează lat/lon |
| `/api/reverse?lat={lat}&lon={lon}` | GET | Geocodare inversă (coordonate → adresă) |
| `/api/route` | POST | Calculează ruta între puncte `{"points": [[lat,lon], ...]}` |
| `/api/export/excel` | POST | Generează fișier XLSX |
| `/api/export/pdf` | POST | Generează fișier PDF |
| `/health` | GET/HEAD | Health check |

---

## 📝 Note

- Starea utilizatorului (vehicule, favorite, istoric) este stocată în `localStorage` — per dispozitiv. Folosește Export JSON pentru backup.
- Cache-ul de geocodare și rutare este stocat pe server în `cache.db` (SQLite) pentru a reduce apelurile externe.
- Serverul este stateless din perspectiva curselor — utilizatorii simultani nu se interferează.
- Pentru volum mare de trafic se recomandă un plan plătit Render și o cheie LocationIQ dedicată.

---
---

# 🇬🇧 English

**Automatic km calculation for trip logs**

🔗 **Live app**: [triplog-05n6.onrender.com](https://triplog-05n6.onrender.com)

> ⚠️ On the free Render tier, the app may take 30–50 seconds to wake up after inactivity.

---

## ✨ Features

- Address autocomplete with OpenStreetMap suggestions
- Automatic distance calculation via OSRM
- Round-trip toggle and multiplier (×) per segment
- Closed-loop option — return to starting point
- Stop reordering via drag-and-drop or up/down buttons
- "My location" button with reverse geocoding
- **Interactive map** (Leaflet) showing the calculated route
- **Vehicle management** — name, plate, fuel consumption, fuel price, driver
- **Cost calculation** per trip based on vehicle consumption
- **Odometer fields** km start / km end (stored in history)
- **Purpose field** per segment
- **Favorites** — save/load frequent routes with JSON export/import
- **Trip history** — all saved trips, filterable by month
- **Monthly Excel report** directly from history
- **Route sharing** via URL (copyable link)
- **New Route button** — quick reset for a new trip without restarting the PWA
- Export to **Excel**, **CSV**, and **PDF**
- 5-tab navigation: Route · Map · Segments · Export · History
- Mobile-first UI, dark/light mode, RO/EN language toggle
- **PWA** — installable on Android and iOS as a native-like app

---

## 🛠️ Tech stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python 3) + uvicorn |
| Frontend | React 18 (CDN, no build step), Babel in-browser |
| Map | Leaflet.js 1.9 |
| Geocoding | LocationIQ → Nominatim → maps.co (cascading fallback) |
| Reverse geocoding | Nominatim `/reverse` |
| Routing | OSRM (router.project-osrm.org) |
| Excel export | pandas + openpyxl |
| PDF export | reportlab |
| Server cache | SQLite via aiosqlite |
| Rate limiting | slowapi (60 req/min per IP) |
| Hosting | Render (free tier) |

---

## 📁 Project structure

```
triplog/
├── main.py              # FastAPI backend
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment config
├── README.md
└── static/
    ├── index.html       # React frontend (single-file SPA)
    ├── manifest.json    # PWA manifest
    ├── sw.js            # Service worker
    ├── icon-192.png     # PWA icon
    └── icon-512.png     # PWA icon
```

---

## 🚀 Local development

1. Clone the repo:
   ```bash
   git clone https://github.com/mrmcb92/triplog.git
   cd triplog
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set environment variables:
   ```bash
   export LOCATIONIQ_KEY="your_key_here"
   export CONTACT_EMAIL="your@email.com"
   export ALLOWED_ORIGINS="https://your-domain.com"
   ```
   Without `LOCATIONIQ_KEY` the app falls back to Nominatim (free, slightly slower).

4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

5. Open [http://localhost:8000](http://localhost:8000).

---

## ☁️ Deployment on Render

The repo includes `render.yaml`. Steps:

1. Create an account at [render.com](https://render.com)
2. New → Web Service → connect this repo
3. Settings are auto-detected from `render.yaml`
4. (Optional) Add Environment Variables:
   - `LOCATIONIQ_KEY` — LocationIQ API key for faster geocoding
   - `CONTACT_EMAIL` — email for Nominatim User-Agent header
   - `ALLOWED_ORIGINS` — allowed CORS origins (default `*`)

---

## 📱 PWA installation

**Android (Chrome):** Open the app → three-dot menu → "Add to Home screen"

**iPhone (Safari):** Open the app in Safari → Share button → "Add to Home Screen"

---

## 🔌 API endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/geocode?q={query}&limit={n}` | GET | Search addresses, returns lat/lon |
| `/api/reverse?lat={lat}&lon={lon}` | GET | Reverse geocode coordinates to address |
| `/api/route` | POST | Calculate route between points `{"points": [[lat,lon], ...]}` |
| `/api/export/excel` | POST | Generate XLSX file |
| `/api/export/pdf` | POST | Generate PDF file |
| `/health` | GET/HEAD | Health check |

---

## 📝 Notes

- User state (vehicles, favorites, history) is stored in `localStorage` — per device. Use JSON export for backup.
- Geocoding and routing results are cached server-side in `cache.db` (SQLite) to reduce external API calls.
- The server is stateless with respect to trips — simultaneous users do not interfere with each other.
- For high traffic, a paid Render plan and a dedicated LocationIQ key are recommended.
