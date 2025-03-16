import PyPDF2

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from io import BytesIO
from typing import Optional

from logger import logger
from settings import db_config

from libintegration.domain.controllers.third_party_integration import ThirdPartyIntegrationController
from libintegration.documentation import document_docs
from libintegration.domain.models import document_model

from .root import responses

document_router = APIRouter(
    prefix="/document",
    # dependencies=[Depends(get_api_version)],
    responses=responses
)

@document_router.post(
    "/upload",
    summary=document_docs.summary,
    tags=["Documents"],
    description=document_docs.upload_descriptions,
    response_model=document_model.DocumentModel,
    include_in_schema=True
)
async def upload_document(
    file: UploadFile,
    db_session = Depends(db_config.get_session)
):
    logger.info(f"Upload documents route with filename: {file.filename}")
    
    try:
        # Read the PDF file into a BytesIO object
        pdf_file = await file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file))
        
        pdf_text = ""
        # Extract text from each page
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"
            
        return {"status": "success", "text": pdf_text}
        
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file"
        )
