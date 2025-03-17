"""Client for interacting with Groq LLM API.

This module provides functions for generating facts from text and matching tags
using the Groq LLM API.
"""

import json
import numpy as np

from groq import Groq
from settings import settings
from sentence_transformers import SentenceTransformer

from schema.tables import Tag
from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import db_config

from libintegration.domain.Constants.doucment import (
    CREATE_FACT_CHUNKS_SYSTEM_PROMPT,
    GET_MATCHING_TAGS_SYSTEM_PROMPT,
    RESPOND_TO_MESSAGE_SYSTEM_PROMPT,
)


class GroqClient:
    def __init__(self):
        self.groq_client = Groq(api_key=settings.LLAMA_API_KEY)
        self.model = None

    async def generate_facts_from_text(self, prompt: str) -> str:
        """Generates facts from input text using Groq LLM.

        Args:
            prompt: Input text to generate facts from.

        Returns:
            str: JSON string containing generated facts.
        """
        response = self.groq_client.chat.completions.create(
            model=settings.LLAMA_MODEL_NAME,
            max_tokens=4000,
            temperature=0.1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": CREATE_FACT_CHUNKS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        llama_facts = json.loads(response.choices[0].message.content)
        return llama_facts.get("facts") or []

    async def get_matching_tags(self, prompt: str, db_session: Session) -> list[str]:
        """Gets matching tags for input text from database.

        Args:
            prompt: Input text to match tags against.
            db_session: Database session object.

        Returns:
            list[str]: List of matching tag IDs.
        """
        tags = db_session.execute(select(Tag)).scalars().all()
        tags_to_match_with = "\n".join([tag.name for tag in tags])
        tags_with_ids = {tag.name: tag.id for tag in tags}

        if not tags_to_match_with:
            return []

        response = self.groq_client.chat.completions.create(
            model=settings.LLAMA_MODEL_NAME,
            max_tokens=4000,
            temperature=0.1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": GET_MATCHING_TAGS_SYSTEM_PROMPT.replace(
                        "{{tags_to_match_with}}", tags_to_match_with
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Parse the response and return the list of tag ids matching with db tags
        llama_tags = json.loads(response.choices[0].message.content).get("tags") or []
        return [
            tag_id
            for tag in llama_tags
            if (tag_id := tags_with_ids.get(tag)) is not None
        ]

    async def generate_embedding(self,text: str) -> list[float]:
        """Generate embedding using sentence-transformers"""
        model = await self.get_embedding_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist() 

    async def get_embedding_model(self):
        if not self.model:
            # Use a model that produces 1536 dimensions
            self.model = SentenceTransformer('BAAI/bge-large-en-v1.5')  # This model outputs 1024 dimensions
        return self.model
