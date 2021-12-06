import uuid
from typing import List, Optional, Union

from fastapi import Response, UploadFile, status

from app.apis.utils.s3uploader import put_file_for_preview
from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import NewRecordResponse, NotFound, UpdatedRecordResponse
from app.models.merchant_offer import (ForbiddenMerchantOfferAccess,
                                       MerchantOfferMerchantView,
                                       MerchantOfferNew,
                                       MerchantOfferNewRequest,
                                       MerchantOfferUpdateRequest)


async def fn_get_merchant_offers(
    email: str,
    merchant_offers_repository: MerchantOffersRepository,
) -> List[MerchantOfferMerchantView]:
    return await merchant_offers_repository.get_merchant_offers(email=email)


async def fn_create_merchant_offer(
    merchant_email: str,
    merchant_offer_new_request: MerchantOfferNewRequest,
    merchants_repository: MerchantsRepository,
    merchant_offers_repository: MerchantOffersRepository,
    response: Response,
) -> Union[NotFound, Optional[NewRecordResponse]]:
    merchant = await merchants_repository.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")
    merchant_offer_new_data = merchant_offer_new_request.dict() | {
        "merchant_id": merchant.id
    }
    merchant_offer_new = MerchantOfferNew(**merchant_offer_new_data)
    merchant_offer_new.before_save()
    return await merchant_offers_repository.create_merchant_offer(
        merchant_offer_new=merchant_offer_new
    )


async def fn_update_merchant_offer(
    merchant_email: str,
    merchant_offer_update_request: MerchantOfferUpdateRequest,
    merchants_repository: MerchantsRepository,
    merchant_offers_repository: MerchantOffersRepository,
    response: Response,
) -> Union[NotFound, ForbiddenMerchantOfferAccess, Optional[UpdatedRecordResponse]]:
    merchant = await merchants_repository.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")

    is_edit_permitted = await merchant_offers_repository.is_merchant_offer_updateable(
        id=merchant_offer_update_request.id, merchant_id=merchant.id
    )
    if not is_edit_permitted.value:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ForbiddenMerchantOfferAccess()

    merchant_offer_update_request.before_save()
    return await merchant_offers_repository.update_merchant_offer(
        merchant_offer_update_request=merchant_offer_update_request
    )


async def fn_update_merchant_offer_status(
    merchant_email: str,
    merchant_offer_id: uuid.UUID,
    status: str,
    merchants_repository: MerchantsRepository,
    merchant_offers_repository: MerchantOffersRepository,
    response: Response,
) -> Union[NotFound, ForbiddenMerchantOfferAccess, Optional[UpdatedRecordResponse]]:
    merchant = await merchants_repository.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")

    is_edit_permitted = await merchant_offers_repository.is_merchant_offer_updateable(
        id=merchant_offer_id, merchant_id=merchant.id
    )
    if not is_edit_permitted.value:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ForbiddenMerchantOfferAccess()

    return await merchant_offers_repository.update_merchant_offer_status(
        id=merchant_offer_id,
        status=status,
    )


async def fn_upload_merchant_offer_image(
    merchant_email: str,
    merchant_offer_id: uuid.UUID,
    file: UploadFile,
    merchants_repository: MerchantsRepository,
    merchant_offers_repository: MerchantOffersRepository,
    response: Response,
) -> int:
    merchant = await merchants_repository.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")

    is_edit_permitted = await merchant_offers_repository.is_merchant_offer_updateable(
        id=merchant_offer_id, merchant_id=merchant.id
    )
    if not is_edit_permitted.value:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ForbiddenMerchantOfferAccess()

    *filename, extension = file.filename.split(".")
    fname = "{}-{}.{}".format(str(merchant_offer_id), "offer_image", extension)
    upload_status = put_file_for_preview(file.file, fname)

    if upload_status == status.HTTP_200_OK:
        await merchant_offers_repository.update_merchant_offer_status(
            id=merchant_offer_id, status="pending_approval"
        )
        # notify_support

    return upload_status
