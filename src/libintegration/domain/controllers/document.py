"""
document_controller.py

This module defines the DocumentController class responsible for handling document-related operations.
"""

from fastapi import UploadFile
from sqlalchemy.orm import Session
from libintegration.domain.enums.providers import LLMProvider
from libintegration.domain.factory.DocumentFactory import DocumentFactory
from libintegration.domain.models import document_model


class DocumentController:
    """Handles document-related operations, including file uploads."""

    async def upload_document(self, file: UploadFile, llm_providers: LLMProvider, db_session: Session):
        """Uploads a document to the specified LLM provider.

        Args:
            file (UploadFile): The document file to be uploaded.
            llm_providers (LLMProvider): The selected Large Language Model (LLM) provider.
            db_session (Session): The database session for managing transactions.

        Returns:
            document_model.DocumentModel: An object containing the upload status and message.

        Raises:
            Exception: If the provider upload process encounters an error.
        """
        provider = DocumentFactory(llm_providers, db_session).get_llm_provider()
        success = await provider.upload_document(file)

        message = (
            f"Document {file.filename} uploaded successfully."
            if success
            else f"Document {file.filename} failed to upload."
        )

        return document_model.DocumentModel(success=success, message=message)
