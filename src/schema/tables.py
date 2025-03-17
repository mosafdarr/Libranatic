from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector

Base = declarative_base()
target_metadata = Base.metadata

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    document_tags = relationship("DocumentTag", back_populates="document")
    document_information_chunks = relationship("DocumentInformationChunk", back_populates="document")

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    document_tags = relationship("DocumentTag", back_populates="tag")

class DocumentTag(Base):
    __tablename__ = 'document_tags'

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'))
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'))
    document = relationship("Document", back_populates="document_tags")
    tag = relationship("Tag", back_populates="document_tags")

class DocumentInformationChunk(Base):
    __tablename__ = 'document_information_chunks'

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'))
    chunk = Column(String)
    embedding = Column(Vector(1024))
    document = relationship("Document", back_populates="document_information_chunks")
