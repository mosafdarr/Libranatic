from fastapi import APIRouter, Depends

from logger import logger
from .root import get_user_code, responses

from libintegration.documentation import users_doc
from libintegration.domain.models import users_model

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