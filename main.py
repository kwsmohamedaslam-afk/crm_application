from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from core.default_data import run_seed
from routers import auth_router, users_router, roles_router, logs_router,department_router,attendance_router,salary_router
import models
from core.db_sync import sync_db

# ── Create all tables on startup (safe no-op if they exist) ──────────────────
Base.metadata.create_all(bind=engine)

# sync_db()  # Sync DB schema with models (add missing columns)

# ── App instance ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="First Project Backend API",
    description=(
        "Complete REST API for the backend system.\n\n"
        "**Authentication**: Use `POST /api/auth/login` to obtain a JWT token, "
        "then click **Authorize** (🔒) and enter `Bearer <token>`."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",)

@app.on_event("startup")
def on_startup():
    print("🚀 Startup begin")

    print("➡️ Running sync_db()")
    sync_db()
    print("✅ sync_db done")

    print("➡️ Running run_seed()")
    run_seed()
    print("✅ run_seed done")

    print("🎉 Startup complete")

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Restrict to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(logs_router)
app.include_router(department_router)
app.include_router(attendance_router)
app.include_router(salary_router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {"status": "ok", "message": "KWS API is running"}
