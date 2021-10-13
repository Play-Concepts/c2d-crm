from typing import Optional

from app.models.core import CoreModel, CreatedAtMixin, IDModelMixin


class CustomerLogBase(CoreModel):
    pda_url: Optional[str]
    event: Optional[str]


CustomerLogNew = CustomerLogBase


class CustomerLogDBModel(IDModelMixin, CustomerLogBase, CreatedAtMixin):
    pass


CustomerLog = CustomerLogDBModel


class CustomerLogNewResponse(IDModelMixin, CreatedAtMixin):
    pass
