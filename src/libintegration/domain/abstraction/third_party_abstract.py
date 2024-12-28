from abc import ABC, abstractmethod
from pydantic import BaseModel

class ThirdPartyAbstract(BaseModel, ABC):
    @abstractmethod
    def get(self):
        """Get Third Party Data"""