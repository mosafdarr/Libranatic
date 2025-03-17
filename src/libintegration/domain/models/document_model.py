from pydantic import BaseModel, Field

class DocumentModel(BaseModel):
    success: bool = Field(default_factory=bool, description="Return true/false determining if document is uploaded or not.")
    message: str = Field(default_factory=str, description="Return a message indicating the status of the document upload.")

class GeneratedDocumentInformationChunks(BaseModel):
    facts: list[str]
