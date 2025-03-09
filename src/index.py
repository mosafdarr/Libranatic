from fastapi import FastAPI
from mangum import Mangum

from libintegration.middlewares.header_middleware import HeaderMiddleware
# from contextlib import asynccontextmanager

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

HeaderMiddleware().add_middleware(app)

# Include Routers
app.include_router(user_router)

async def health():
    """
    Health check endpoint to verify if the application is running properly.
    """
async def health():
    return {"message": "Application's health is good."}

handler = Mangum(app, lifespan="off", api_gateway_base_path="/")
