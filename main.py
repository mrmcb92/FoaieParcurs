from __future__ import annotations
import io, math, os
from typing import List, Tuple, Dict, Optional

import requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import pandas as pd

app = FastAPI(title="Foaie de parcurs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LOCATIONIQ_KEY = os.getenv("LOCATIONIQ_KEY", "") or os.getenv("LOCATIONIQ_TOKEN", "")
CONTACT_EMAIL  = os.getenv("CONTACT_EMAIL", "")
USER_AGENT     = f"FoaieParcursApp/8.0 (contact:{CONTACT_EMAIL or 'none'})"

# Cache in-memory simplu (per proces, se pierde la restart - acceptabil)
_geo_cache: Dict[str, list] = {}
_rte_cache: Dict[str, dict] = {}


def km_round(x: float) -> float:
    """Rotunjire aritmetică standard (evită banker's rounding din Python)."""
    return math.floor(x * 10 + 0.5) / 10


# ---- Geocodare ----

def _try_locationiq(q: str, limit: int) -> Optional[list]:
    if not LOCATIONIQ_KEY:
        return None
    try:
        r = requests.get(
            "https://us1.locationiq.com/v1/search",
            params={"key": LOCATIONIQ_KEY, "q": q, "format": "json",
                    "normalizecity": 1, "limit": str(limit), "accept-language": "ro"},
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        r.raise_for_status()
        js = r.json()
        if not isinstance(js, list):
            return None
        return [{"lat": float(it["lat"]), "lon": float(it["lon"]),
                 "display": it.get("display_name", q)} for it in js]
    except Exception:
        return None


def _try_nominatim(q: str, limit: int) -> Optional[list]:
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": q, "format": "json", "limit": limit, "accept-language": "ro"},
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        r.raise_for_status()
        js = r.json()
        if not isinstance(js, list):
            return None
        return [{"lat": float(it["lat"]), "lon": float(it["lon"]),
                 "display": it.get("display_name", q)} for it in js]
    except Exception:
        return None


def _try_mapsco(q: str, limit: int) -> Optional[list]:
    try:
        r = requests.get(
            "https://geocode.maps.co/search",
            params={"q": q, "limit": str(limit)},
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        r.raise_for_status()
        js = r.json()
        if not isinstance(js, list):
            return None
        out = []
        for it in js:
            if it.get("lat") and it.get("lon"):
                out.append({
                    "lat": float(it["lat"]),
                    "lon": float(it["lon"]),
                    "display": it.get("display_name") or it.get("name") or q,
                })
        return out or None
    except Exception:
        return None


@app.get("/api/geocode")
async def geocode(q: str = Query(..., min_length=3), limit: int = Query(6, ge=1, le=10)):
    key = f"{q}|{limit}"
    if key in _geo_cache:
        return {"results": _geo_cache[key]}

    result = _try_locationiq(q, limit) or _try_nominatim(q, limit) or _try_mapsco(q, limit) or []
    _geo_cache[key] = result
    return {"results": result}


# ---- Rutare ----

class RouteRequest(BaseModel):
    points: List[Tuple[float, float]]


@app.post("/api/route")
async def route(body: RouteRequest):
    if len(body.points) < 2:
        raise HTTPException(400, "Minim 2 puncte necesare.")

    key = "|".join(f"{la:.5f},{lo:.5f}" for la, lo in body.points)
    if key in _rte_cache:
        return _rte_cache[key]

    coord_str = ";".join(f"{lo},{la}" for la, lo in body.points)
    url = (
        f"https://router.project-osrm.org/route/v1/driving/{coord_str}"
        f"?overview=full&alternatives=false&steps=false&geometries=geojson"
    )

    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
        if r.status_code == 400:
            d = r.json()
            raise HTTPException(400, d.get("message", "Nu s-a găsit rută."))
        r.raise_for_status()
        data = r.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(503, f"Eroare rețea OSRM: {e}")

    routes = data.get("routes") or []
    if not routes:
        raise HTTPException(404, "Nicio rută găsită.")

    legs    = routes[0].get("legs", [])
    legs_km = [km_round(leg["distance"] / 1000) for leg in legs]

    geom   = routes[0].get("geometry", {})
    raw    = geom.get("coordinates", []) if geom.get("type") == "LineString" else []
    coords = raw[::3]
    if raw and (not coords or coords[-1] != raw[-1]):
        coords.append(raw[-1])

    result = {"legs_km": legs_km, "coords": coords}
    _rte_cache[key] = result
    return result


# ---- Export Excel ----

class ExportRequest(BaseModel):
    rows: List[Dict]
    total: float
    date_str: str


@app.post("/api/export/excel")
async def export_excel(body: ExportRequest):
    df  = pd.DataFrame(body.rows)
    bio = io.BytesIO()
    try:
        from openpyxl.styles import Font
        from openpyxl.utils import get_column_letter
        with pd.ExcelWriter(bio, engine="openpyxl") as w:
            df.to_excel(w, index=False, header=False,
                        sheet_name="Foaie de parcurs", startrow=1)
            ws = w.sheets["Foaie de parcurs"]
            for i, col in enumerate(df.columns, 1):
                ws.cell(1, i, col).font = Font(bold=True)
            tc = df.shape[1] + 1
            ws.cell(1, tc, "KM totali").font = Font(bold=True)
            ws.cell(2, tc, float(body.total)).font = Font(bold=True)
            ws.cell(2, tc).number_format = "0.0"
            ws.column_dimensions[get_column_letter(tc)].width = 15
            ws.freeze_panes = "A2"
    except Exception as e:
        raise HTTPException(500, str(e))

    bio.seek(0)
    fname = f"foaie_parcurs_{body.date_str}.xlsx"
    return StreamingResponse(
        bio,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={fname}"},
    )


# ---- Health check ----

@app.get("/health")
@app.head("/health")
async def health():
    return {"status": "ok"}


# ---- Service Worker (trebuie servit cu header Service-Worker-Allowed) ----

from fastapi.responses import Response as FastAPIResponse

@app.get("/static/sw.js")
async def service_worker():
    with open("static/sw.js", "r") as f:
        content = f.read()
    return FastAPIResponse(
        content=content,
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"},
    )


# ---- Static / SPA ----

INDEX_PATH = os.path.join("static", "index.html")

if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse(INDEX_PATH)


@app.get("/{full_path:path}")
async def spa(full_path: str):
    # Nu interceptăm rutele API
    if full_path.startswith("api/"):
        raise HTTPException(404, "Not found")
    return FileResponse(INDEX_PATH)
