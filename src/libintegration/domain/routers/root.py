from fastapi import Header
from typing import Optional
from libintegration.domain.models.error_model import IntegrationErrorModel

async def get_user_code(
        x_user_code: Optional[str] = Header(default=None, title="User Code")
):
    return x_user_code

responses = {
    400: {"model": IntegrationErrorModel, "description": "Bad Request"},
    401: {"model": IntegrationErrorModel, "description": "Unauthorized"},
    403: {"model": IntegrationErrorModel, "description": "Forbidden"},
    404: {"model": IntegrationErrorModel, "description": "Not Found"},
    422: {"model": IntegrationErrorModel, "description": "Unprocessable Entity"},
    429: {"model": IntegrationErrorModel, "description": "Too Many Requests"},
    500: {"model": IntegrationErrorModel, "description": "Internal Server Error"},
    501: {"model": IntegrationErrorModel, "description": "Not Implemented"},
}
