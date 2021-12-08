from pydantic.main import BaseModel


class InsufficientFundsException(Exception):
    pass


class InsufficientFundsResponse(BaseModel):
    message: str = "Insufficient Funds"
