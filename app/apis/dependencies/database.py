from typing import Callable, Type, Any
from databases import Database
from fastapi import Depends
from starlette.requests import Request

from app.db.repositories.base import BaseRepository


def get_database(request: Request) -> Database:
    return request.app.state.db


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Any:
        return repo_type(db)

    return get_repo
