import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Leaflet WebApp Backend", version="1.0.0")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DIST_DIR = BASE_DIR / "frontend" / "dist"
ASSETS_DIR = DIST_DIR / "frontend" / "browser"


@app.get("/api/status")
def status():
    return {"status": "online"}


app.mount("/", StaticFiles(directory=ASSETS_DIR, html=True), name="static")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
