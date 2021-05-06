from pydantic import BaseModel


class Customer(BaseModel):
    id: str
    name: str
