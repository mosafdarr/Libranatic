from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# from app.database import engine, Base
from libintegration.domain.routers import user_router
# from app.auth import routes as auth_routes
from settings import settings

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Create database tables on startup
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     # Any cleanup code can go here

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Comprehensive FastAPI Project Template",
    version="0.1.0",
    # lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include Routers
# app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Application"}