import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from mangum import Mangum
from settings import settings

from libintegration.middlewares.header_middleware import HeaderMiddleware
from libintegration.domain.routers import document_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Library integration API",
    version="0.1.0",
    # lifespan=lifespan
)

HeaderMiddleware().add_middleware(app)

# Include Routers
app.include_router(document_router)

async def health():
    """
    Health check endpoint to verify if the application is running properly.
    """
    return {"message": "Application's health is good."}

handler = Mangum(app, lifespan="off", api_gateway_base_path="/")
