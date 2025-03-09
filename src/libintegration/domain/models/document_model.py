from pydantic import BaseModel, Field

class DocumentModel(BaseModel):
    message: bool = Field(default_factory=bool, description="Return true/false determining if document is uploaded or not.")