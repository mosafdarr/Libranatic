from fastapi import HTTPException, status
from logger import logger

from sqlalchemy.orm import Session

from libintegration.domain.enums.providers import LLMProvider
from libintegration.domain.apps.document_parsing.groq.document_app import GroqDocumentApp


class DocumentFactory:
    """Factory class for creating document processing services based on the LLM provider.

    Args:
        service_provider (LLMProvider): The selected LLM provider.
        db_session (Session): The database session for managing transactions.
    """

    service_provider: LLMProvider = None
    db_session: Session = None

    def __init__(self, service_provider: LLMProvider, db_session: Session):
        """Initializes the DocumentFactory with the specified service provider and database session."""
        self.service_provider = service_provider
        self.db_session = db_session

    def get_llm_provider(self):
        """Retrieves the appropriate document processing service based on the provider.

        Returns:
            GroqDocumentApp: An instance of the document processing application.

        Raises:
            HTTPException: If the specified provider is not implemented.
        """
        logger.info(f"DocumentFactory - service provider: {self.service_provider}")

        if self.service_provider == LLMProvider.GROQ:
            return GroqDocumentApp(db_session=self.db_session)

        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={"message": "This service provider is not implemented"},
        )
