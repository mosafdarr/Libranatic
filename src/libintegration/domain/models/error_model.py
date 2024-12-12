from pydantic import Field, BaseModel


class ErrorModelDetail(BaseModel):
    code: str = Field(None, description="Error code")
    message: str = Field(None, description="Error message")
    object: str = Field(None, description="Error object")

class IntegrationErrorModel(BaseModel):
    details: ErrorModelDetail = Field(None, description="Error details")
