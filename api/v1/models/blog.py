#!/usr/bin/env python3
""" The Blog Post Model
"""
from sqlalchemy import (
        Column,
        Integer,
        String,
        Text,
        Date,
        ForeignKey,
        DateTime,
        func,
        Boolean
        )
from sqlalchemy.orm import relationship
from datetime import datetime
from api.v1.models.base import Base
from api.v1.models.base_model import BaseModel
from uuid_extensions import uuid7
from sqlalchemy.dialects.postgresql import UUID, ARRAY


class Blog(BaseModel, Base):
    __tablename__ = 'blogs'

    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    image_url = Column(String(100), nullable=True)
    tags = Column(ARRAY(String(20)), nullable=True)

    author = relationship("User", backref="blogs")
