from fastapi import HTTPException, status
from logger import logger
from sqlalchemy.orm import Session

from libintegration.domain.enums.providers import TestProvider
from libintegration.domain.apps.third_party_integration_app.third_party_integration import ThirdPartyIntegration

class TestFactory:
    """This factory class will be used as an abstract factory pattern to all test third party integrations"""

    service_provider: str = None
    db_session: Session = None

    def __init__(
        self,
        service_provider,
        db_session: Session
    ):
        self.service_provider = service_provider
        self.db_session = db_session
    
    def get_test_provider(self):
        logger.info(f"TestFactory - service provider {self.service_provider}")
        if self.service_provider == TestProvider.TEST1:
            return ThirdPartyIntegration(db_session=self.db_session)
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={"message": "This service provider is not implemented"}
        )