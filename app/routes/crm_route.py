from typing import Dict, List

from app.apis.crm.mainmod import fn_get_customer, fn_list_customers
from app.models.customer import Customer
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user


router = APIRouter()


@router.get("/crm/customers", tags=["crm"])
async def list_customers(auth=Depends(get_current_user)) -> List[Customer]:
    return fn_list_customers()


@router.post("/crm/customers", tags=["crm"])
async def save_customer(customer: Customer, auth=Depends(get_current_user)) -> Customer:
    return customer


@router.get("/crm/customers/{customer_id}", tags=["crm"])
async def get_customer(customer_id: str, auth=Depends(get_current_user)) -> Customer:
    return fn_get_customer(customer_id)


@router.post("/crm/upload", tags=["crm"])
async def upload(customer: Customer, auth=Depends(get_current_user)) -> Customer:
    return customer

