import uuid
from typing import List, Optional, Union

from fastapi import Response, UploadFile, status

from app.apis.utils.s3uploader import put_file_for_preview
from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.db.repositories.merchant_offers_data_passes import \
    MerchantOffersDataPassesRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import NewRecordResponse, NotFound, UpdatedRecordResponse
from app.models.merchant_offer import (ForbiddenMerchantOfferAccess,
                                       MerchantOfferMerchantView,
                                       MerchantOfferNew,
                                       MerchantOfferNewRequest,
                                       MerchantOfferUpdate,
                                       MerchantOfferUpdateRequest)
from app.models.merchant_offer_data_pass import MerchantOfferDataPassNew


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
    merchant_offers_data_passes_repository: MerchantOffersDataPassesRepository,
    response: Response,
) -> Union[NotFound, Optional[NewRecordResponse]]:
    merchant = await merchants_repository.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")
    merchant_offer_new_data = merchant_offer_new_request.dict() | {
        "merchant_id": merchant.id
    }
    data_passes = merchant_offer_new_data.pop("data_passes")

    merchant_offer_new = MerchantOfferNew(**merchant_offer_new_data)
    merchant_offer_new.before_save()
    merchant_offer = await merchant_offers_repository.create_merchant_offer(
        merchant_offer_new=merchant_offer_new
    )
    for data_pass in data_passes:
        await merchant_offers_data_passes_repository.create_merchant_offer_data_pass(
            merchant_offer_data_pass_new=MerchantOfferDataPassNew(
                merchant_offer_id=merchant_offer.id,
                data_pass_id=data_pass,
            )
        )
    return merchant_offer


async def fn_update_merchant_offer(
    merchant_email: str,
    merchant_offer_id: uuid.UUID,
    merchant_offer_update_request: MerchantOfferUpdateRequest,
    merchants_repository: MerchantsRepository,
    merchant_offers_repository: MerchantOffersRepository,
    merchant_offers_data_passes_repository: MerchantOffersDataPassesRepository,
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

    merchant_offer_update_data = merchant_offer_update_request.dict() | {
        "id": merchant_offer_id,
    }
    data_passes = merchant_offer_update_data.pop("data_passes")

    merchant_offer_update = MerchantOfferUpdate(**merchant_offer_update_data)
    merchant_offer_update.before_save()
    merchant_offer = await merchant_offers_repository.update_merchant_offer(
        merchant_offer_update=merchant_offer_update
    )

    await merchant_offers_data_passes_repository.disable_all_merchant_offer_data_passes(
        merchant_offer_id=merchant_offer.id,
    )

    for data_pass in data_passes:
        await merchant_offers_data_passes_repository.create_merchant_offer_data_pass(
            merchant_offer_data_pass_new=MerchantOfferDataPassNew(
                merchant_offer_id=merchant_offer.id,
                data_pass_id=data_pass,
            )
        )

    return merchant_offer


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
