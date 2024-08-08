#!/usr/bin/python3
"""
This module defines the User class, which inherits from the BaseModel class.
"""
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

parent_classes = (
    BaseModel,
    Base if STORAGE_TYPE == "db" else object
)


class User(*parent_classes):
    """
    User class represents a user.
    """
    NOT_UPDATABLE = ['email']

    if STORAGE_TYPE == "db":
        __tablename__ = 'users'

        email = Column(String(128), nullable=False, index=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), index=True)
        last_name = Column(String(128), index=True)
        places = relationship('Place', back_populates='user',
                              passive_deletes=True)
        reviews = relationship('Review', back_populates='user',
                               passive_deletes=True)

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
