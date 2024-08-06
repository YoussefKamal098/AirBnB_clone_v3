#!/usr/bin/python3
"""
This module defines the City class,
which represents a city in the context of a geographic location.
"""
import os

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

parent_classes = (
    BaseModel,
    Base if STORAGE_TYPE == "db" else object
)


class City(*parent_classes):
    """
    City class represents a city within a geographic location.
    """

    NOT_UPDATABLE = ['state_id']

    if STORAGE_TYPE == "db":
        __tablename__ = 'cities'

        name = Column(String(128), nullable=False, index=True)
        state_id = Column(String(60),
                          ForeignKey('states.id', ondelete="CASCADE"),
                          nullable=False)
        state = relationship("State", back_populates="cities")
        places = relationship('Place', back_populates='city',
                              passive_deletes=True)

        __table_args__ = (
            UniqueConstraint('name', 'state_id', name='_name_state_id_uc'),
        )
    else:
        name: str = ""
        state_id: str = ""

    def update(self, **kwargs):
        """
        Updates the City instance with the key/value pairs in kwargs.

        This method updates only the attributes of the City instance
        that can be updated.

        Parameters:
            **kwargs (dict): Arbitrary keyword arguments.
        """

        for attr in self.__class__.NOT_UPDATABLE:
            kwargs.pop(attr, None)

        super().update(self, **kwargs)
