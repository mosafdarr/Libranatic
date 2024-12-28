from pydantic import BaseModel
from logger import logger
from sqlalchemy.orm import Session

from libintegration.domain.factory.third_party_factory import TestFactory


class ThirdPartyIntegrationController(BaseModel):
    def get_third_party_data(
        self,
        params: str,
        service_provider,
        db_session: Session
    ):
        logger.info(f"Query Pram {params}")
        test_provider = TestFactory(
            service_provider=service_provider, db_session=db_session
        ).get_test_provider()
        return test_provider.get(params)