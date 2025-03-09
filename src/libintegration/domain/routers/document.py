from fastapi import APIRouter, Depends

from logger import logger
from settings import db_config

from schema.tables import User

from libintegration.domain.controllers.third_party_integration import ThirdPartyIntegrationController
from libintegration.documentation import users_doc
from libintegration.domain.models import users_model

from .root import get_user_code, get_test_providers, responses

document_router = APIRouter(
    prefix="/document",
    # dependencies=[Depends(get_api_version)],
    responses=responses
)

@document_router.get(
        "/",
        summary=users_doc.summary,
        tags=["Users"],
        description=users_doc.descriptions,
        response_model=users_model.UserResponseModel,
        include_in_schema=True
)
def test_get_third_party_data(
    query_param: str,
    user_code=Depends(get_user_code),
    service_provider=Depends(get_test_providers),
    db_session=Depends(db_config.get_session)
):
    logger.info(f"Your User code is {user_code}")
    test_data = ThirdPartyIntegrationController()
    return test_data.get_third_party_data(query_param, service_provider, db_session)
