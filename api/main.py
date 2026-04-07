"""
FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import connect, disconnect, get_db
from api.routers import heroes, items, strategies, version


# ── Lifespan: connect to MongoDB on startup, disconnect on shutdown ──
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await disconnect()


# ── Create the app ──
app = FastAPI(
    title="MLBB Guide API",
    description="REST API serving Mobile Legends: Bang Bang hero, item, and strategy data from MongoDB Atlas.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS — allow all origins in development ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ──
app.include_router(heroes.router)
app.include_router(items.router)
app.include_router(strategies.router)
app.include_router(version.router)


# ── Root health check ──
@app.get("/", tags=["Health"])
async def root():
    """API health check — also verifies database connectivity."""
    try:
        db = get_db()
        await db.command("ping")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "ok",
        "service": "MLBB Guide API",
        "version": "1.0.0",
        "database": db_status,
    }
