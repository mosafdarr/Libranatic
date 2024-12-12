from pydantic import BaseModel, Field
from typing import List, Optional

class UserResponseModel(BaseModel):
    message: List[str] = Field(default_factory=list, description="List of all users")