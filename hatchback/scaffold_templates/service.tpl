from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.__resource__ import __Resource__Repository

class __Resource__Service:
    def __init__(self, db: Session):
        self.repo = __Resource__Repository(db)

    def get(self, id: UUID):
        return self.repo.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def create(self, data: dict):
        return self.repo.create(data)

    def update(self, id: UUID, data: dict):
        return self.repo.update(id, data)

    def delete(self, id: UUID):
        return self.repo.delete(id)
