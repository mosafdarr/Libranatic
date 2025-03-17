"""
groq_document_app.py

This module defines the GroqDocumentApp class for processing and uploading PDF documents.
"""

import asyncio
import PyPDF2

from io import BytesIO
from itertools import chain
from fastapi import UploadFile

from sqlalchemy.orm import Session
from schema.tables import Document, DocumentInformationChunk, DocumentTag
from libintegration.domain.apps.document_parsing.groq.groq_client import GroqClient


class GroqDocumentApp:
    """Handles document processing, including text extraction, chunking, and database insertion."""

    def __init__(self, db_session: Session):
        """Initializes the document app with a database session and Groq client."""
        self.groq_client = GroqClient()
        self.db_session: Session = db_session
        self.ideal_chunk_length = 4000

    async def upload_document(self, file: UploadFile) -> bool:
        """Processes and uploads a PDF document.

        Args:
            file (UploadFile): The PDF file to be processed.

        Returns:
            bool: True if the document was uploaded successfully, otherwise False.
        """
        pdf_text = await self.extract_text_from_pdf(file)
        pdf_text_chunks = await self.split_text_into_chunks(pdf_text)

        # Prepare coroutines to generate document facts and retrieve relevant tags concurrently
        generate_facts_coroutines = [
            self.groq_client.generate_facts_from_text(chunk) for chunk in pdf_text_chunks
        ]
        get_matching_tags_coroutine = self.groq_client.get_matching_tags(pdf_text[:5000], self.db_session)

        # Execute fact generation and tag retrieval in parallel
        [document_chunks, matching_tag_ids] = await asyncio.gather(
            asyncio.gather(*generate_facts_coroutines), get_matching_tags_coroutine
        )

        # Flatten the list of generated document chunks
        document_information_chunks = list(chain.from_iterable(document_chunks))

        # Store document into db
        try:
            document_id = await self.insert_document_name_into_db(file.filename)
            await self.insert_document_chunks_into_db(document_id, document_information_chunks)
            await self.insert_document_tags_into_db(document_id, matching_tag_ids)

            # Commit the transaction if everything succeeds
            self.db_session.commit()
            return True

        except Exception:
            # Rollback in case of an error
            self.db_session.rollback()
            return False


    async def split_text_into_chunks(self, text: str) -> list[str]:
        """Splits extracted text into smaller chunks.

        Args:
            text (str): The text to split.

        Returns:
            list[str]: A list of text chunks.
        """
        return [text[i : i + self.ideal_chunk_length] for i in range(0, len(text), self.ideal_chunk_length)]

    async def extract_text_from_pdf(self, file: UploadFile) -> str:
        """Extracts text from a PDF file.

        Args:
            file (UploadFile): The PDF file.

        Returns:
            str: Extracted text from the PDF.
        """
        pdf_file = await file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file))
        return "\n\n".join(page.extract_text() for page in pdf_reader.pages)

    async def insert_document_name_into_db(self, file_name: str) -> int:
        """Inserts a document name into the database.

        Args:
            file_name (str): The name of the document.

        Returns:
            int: The ID of the newly inserted document.
        """
        document = Document(name=file_name)
        self.db_session.add(document)
        self.db_session.flush()
        return document.id

    async def insert_document_chunks_into_db(self, document_id: int, document_information_chunks: list[DocumentInformationChunk]):
        """Inserts document chunks into the database.

        Args:
            document_id (int): The ID of the document.
            document_information_chunks (list[DocumentInformationChunk]): Chunks to insert.
        """
        for chunk in document_information_chunks:
            chunk_obj = DocumentInformationChunk(
                document_id=document_id,
                chunk=chunk,
                embedding=await self.groq_client.generate_embedding(chunk),
            )
            self.db_session.add(chunk_obj)

    async def insert_document_tags_into_db(self, document_id: int, matching_tag_ids: list[int]):
        """Inserts document tags into the database.

        Args:
            document_id (int): The ID of the document.
            matching_tag_ids (list[int]): List of tag IDs to associate with the document.
        """
        for tag_id in matching_tag_ids:
            tag_obj = DocumentTag(document_id=document_id, tag_id=tag_id)
            self.db_session.add(tag_obj)
