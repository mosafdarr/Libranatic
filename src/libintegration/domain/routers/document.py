"""
document_router.py

This module defines API routes for document-related operations in the FastAPI application.

Routes:
    - POST /document/upload: Uploads a document for processing.
"""

from fastapi import APIRouter, Depends, UploadFile
from logger import logger
from settings import db_config
from libintegration.domain.controllers.document import DocumentController
from libintegration.documentation import document_docs
from libintegration.domain.models import document_model
from .root import responses, get_llm_providers

IDEAL_CHUNK_LENGTH = 4000

document_router = APIRouter(
    prefix="/document",
    responses=responses
)

@document_router.post(
    "/upload",
    summary=document_docs.summary,
    tags=["Documents"],
    description=document_docs.upload_descriptions,
    response_model=document_model.DocumentModel,
    responses=responses,
    include_in_schema=True
)
async def upload_document(
    file: UploadFile,
    db_session=Depends(db_config.get_session),
    service_provider=Depends(get_llm_providers)
):
    """Handles document uploads.

    Args:
        file (UploadFile): The file to be uploaded.
        db_session (Session, optional): Database session dependency.
        service_provider (Any, optional): Service provider dependency.

    Returns:
        document_model.DocumentModel: The uploaded document's metadata and processing result.

    Raises:
        HTTPException: If the upload fails.
    """
    logger.info(f"Upload documents route with filename: {file.filename}")
    response = await DocumentController().upload_document(file, service_provider, db_session)
    return response
