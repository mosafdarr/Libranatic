from fastapi import APIRouter, Depends, UploadFile, File

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
def upload_document(
    db_session = Depends(db_config.get_session),
    file: UploadFile = File(...)
):
    logger.info(f"Upload documents route with filename: {file.filename}")
    # test_data = ThirdPartyIntegrationController()
    # # Process the uploaded file here
    # file_content = await file.read()
    # You can add logic to handle the file content as needed
    # return test_data.get_third_party_data(query_param, service_provider, db_session)
    return True
