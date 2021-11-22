from pydantic.main import BaseModel


class PaymentIntent(BaseModel):
    amount: int
    currency: str
