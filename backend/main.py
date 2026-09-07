import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from .api.routes import router as api_router
from .config import BASE_DIR, APP_PORT, APP_HOST

app = FastAPI(
    title="CareerTwin AI API",
    description="Multi-Agent AI Career Digital Twin Platform for Students",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# No-cache middleware to ensure browser always executes latest frontend code
@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Include API Router
app.include_router(api_router)

# Static files and frontend serving
frontend_dir = BASE_DIR / "frontend"
frontend_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "CareerTwin AI",
        "version": "1.0.0"
    }

@app.get("/")
async def serve_index():
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file), headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        })
    return {
        "message": "CareerTwin AI Backend is running."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=APP_HOST, port=APP_PORT, reload=True)
