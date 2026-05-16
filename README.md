# Foaie de parcurs — calcul automat km 🚗

Aplicație web pentru generarea foilor de parcurs cu distanțe calculate automat folosind OSRM (varianta gratuită OpenStreetMap).

🔗 **Aplicație live**: [foaieparcurs.onrender.com](https://foaieparcurs.onrender.com)

> ⚠️ La prima accesare după o perioadă de inactivitate, aplicația poate dura 30-50 de secunde să pornească (limitare a planului gratuit Render).

---

## ✨ Funcționalități

- Introducerea punctului de plecare și a opririlor intermediare
- Autocomplete pentru adrese cu sugestii din OpenStreetMap
- Calcul automat al distanțelor dintre adrese prin OSRM
- Bifare „dus-întors" și multiplicare pe fiecare segment
- Închidere circuit (revenire la punctul de plecare)
- Reordonare și ștergere opriri
- Favorite salvate local în browser, cu export/import JSON
- Export în **Excel** și **CSV** cu total km inclus
- Interfață mobile-first cu navigare în tab-uri

---

## 🛠️ Stack tehnic

- **Backend**: FastAPI (Python 3)
- **Frontend**: React (fără build step, servit de FastAPI)
- **Geocodare**: LocationIQ (cu fallback pe Nominatim și maps.co)
- **Rutare**: OSRM (router.project-osrm.org)
- **Hosting**: Render

---

## 📁 Structura proiectului

```
FoaieParcurs/
├── main.py              # Backend FastAPI (geocodare, rutare, export)
├── requirements.txt     # Dependențe Python
├── render.yaml          # Configurare deployment Render
├── README.md
└── static/
    └── index.html       # Frontend React (single-file)
```

---

## 🚀 Rulare locală

Dacă vrei să rulezi aplicația pe propriul calculator:

1. Clonează repo-ul:
   ```bash
   git clone https://github.com/mrmcb92/FoaieParcurs.git
   cd FoaieParcurs
   ```

2. Instalează dependențele:
   ```bash
   pip install -r requirements.txt
   ```

3. (Opțional) Setează variabilele de mediu pentru LocationIQ:
   ```bash
   export LOCATIONIQ_KEY="cheia_ta_aici"
   export CONTACT_EMAIL="email@example.com"
   ```
   Fără aceste variabile, aplicația folosește Nominatim ca fallback.

4. Pornește serverul:
   ```bash
   uvicorn main:app --reload
   ```

5. Deschide [http://localhost:8000](http://localhost:8000) în browser.

---

## ☁️ Deployment pe Render

Repo-ul include `render.yaml` cu configurarea de bază. Pentru deployment:

1. Creează un cont pe [render.com](https://render.com)
2. New → Web Service → conectează acest repo
3. Setări (sau le preia automat din `render.yaml`):
   - Language: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. (Opțional) Adaugă în Environment Variables:
   - `LOCATIONIQ_KEY` — cheia API LocationIQ
   - `CONTACT_EMAIL` — email pentru User-Agent

---

## 🔌 API endpoints

Backend-ul expune trei endpoint-uri:

| Endpoint | Metodă | Descriere |
|----------|--------|-----------|
| `/api/geocode?q={query}` | GET | Caută adrese, returnează lat/lon |
| `/api/route` | POST | Calculează ruta între puncte (corp JSON: `{points: [[lat, lon], ...]}`) |
| `/api/export/excel` | POST | Generează fișier XLSX |

---

## 📝 Note

- Aplicația respectă limitele de utilizare ale providerilor de geocodare gratuită (Nominatim: 1 req/sec).
- Datele favorite sunt stocate în `localStorage` din browser, deci sunt per-dispozitiv. Folosește Export JSON pentru backup.
- Pentru utilizare comercială intensă, recomand un plan plătit LocationIQ și instanță plătită Render.
