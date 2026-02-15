import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Load environment variables from .env file BEFORE importing auth module
if os.getenv("ENVIRONMENT") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Import auth components (after env vars are loaded)
from auth import router as auth_router, AuthMiddleware


app = FastAPI(title="Leaflet WebApp Backend", version="1.0.0")
app.add_middleware(AuthMiddleware)
app.include_router(auth_router)


@app.get("/api/status")
def status():
    return {"status": "online"}


# Serve static files from the frontend build (dist) directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "frontend" / "dist" / "frontend" / "browser"
app.mount("/", StaticFiles(directory=ASSETS_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
