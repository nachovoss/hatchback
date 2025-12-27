from app.models.__resource__ import __Resource__
from app.repositories.base import BaseRepository

class __Resource__Repository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, __Resource__)
