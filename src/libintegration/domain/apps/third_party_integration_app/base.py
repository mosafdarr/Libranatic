import json

from pydantic import BaseModel
from functools import wraps
from fastapi import HTTPException
from logger import logger

from sqlalchemy.orm import Session

from libintegration.domain.enums.providers import TestProvider

class ThirdPartyBase(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    db_session: Session = None
    base_url: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_session = kwargs.pop("db_session", None)
        self.base_url = "https://linkedin-data-api.p.rapidapi.com"
    
    def get_header(self):
        return {
            'x-rapidapi-host': 'linkedin-data-api.p.rapidapi.com',
            'x-rapidapi-key': '24aea9356dmshbed8897e1610356p1a3e96jsnf68c717c2a34'
        }
    
    def get_token(self):
        pass


def third_party_exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as error:
            response_dict = error.response.__dict__
            logger.info(f"ThirdParty Errors - {func.__name__} {response_dict}")

            content_bytes = response_dict.get("_content")
            content_str = content_bytes.decode("UTF-8")

            error_message = None
            content_dict = json.loads(content_str) if content_str else {}
            error_message = content_dict.get("message") or content_dict.get("error_description")

            if not error_message and content_dict.get("issues"):
                error_message = ",".join(content_dict.get("issues"))
            
            raise HTTPException(
                status_code=response_dict.get("status_code"),
                detail={"message": error_message or response_dict.get("reason")}
            )from error

    return wrapper
