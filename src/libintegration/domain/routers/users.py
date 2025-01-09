from fastapi import APIRouter, Depends

from logger import logger
from .root import get_user_code, get_test_providers, responses

from settings import db_config
from libintegration.domain.controllers.third_party_integration import ThirdPartyIntegrationController
from libintegration.documentation import users_doc
from libintegration.domain.models import users_model
from schema.tables import User

user_router = APIRouter(
    prefix="/users",
    # dependencies=[Depends(get_api_version)],
    responses=responses
)

@user_router.get(
        "/",
        summary=users_doc.summary,
        tags=["Users"],
        description=users_doc.descriptions,
        response_model=users_model.UserResponseModel,
        include_in_schema=True
)
def read_users(
    # db_sesssion=Depends(get_sesssion), - for database sessions
    # service_provider=Depends(get_service_provider), 
    user_code=Depends(get_user_code)
):
    logger.info(f"Your User code is {user_code}")
    return users_model.UserResponseModel(message=["user1", "user2"])

@user_router.get(
        "/test_third_party",
        summary="Test Third Party Integration",
        tags=["Test Route"],
        description="This route is configure as test to third party integrations.",
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

@user_router.get(
        "/test1-lambda",
        summary="Test Route 1",
        tags=["Test Route"],
        description="This route is configure as test to third party integrations.",
        include_in_schema=True
)
def read_users(
    # db_sesssion=Depends(get_sesssion), - for database sessions
    # service_provider=Depends(get_service_provider), 
    user_code=Depends(get_user_code)
):
    logger.info(f"Your User code is {user_code}")
    return users_model.UserResponseModel(message=["user1", "user2"])
