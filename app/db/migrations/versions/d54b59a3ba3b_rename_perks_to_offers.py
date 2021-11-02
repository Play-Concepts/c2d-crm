"""rename_perks_to_offers
Revision ID: d54b59a3ba3b
Revises: d58926c0c666
Create Date: 2021-11-02 17:16:39.517105
"""
from alembic import op

# revision identifiers, used by Alembic
revision = "d54b59a3ba3b"
down_revision = "d58926c0c666"
branch_labels = None
depends_on = None


def _rename_tables(reverse: bool):
    for perk, offer in [
        ("merchant_perks", "merchant_offers"),
        ("merchant_perk_favourites", "merchant_offer_favourites"),
        ("merchant_perks_data_passes", "merchant_offers_data_passes"),
    ]:
        if reverse:
            op.rename_table(offer, perk)
        else:
            op.rename_table(perk, offer)


def _rename_columns(reverse: bool):
    for table, perk, offer in [
        ("merchant_offers", "perk_url", "offer_url"),
        ("merchant_offers", "perk_image_url", "offer_image_url"),
        ("data_passes", "perks_url_for_merchants", "offers_url_for_merchants"),
        ("data_passes", "perks_url_for_customers", "offers_url_for_customers"),
        ("merchant_offer_favourites", "merchant_perk_id", "merchant_offer_id"),
        ("merchant_offers_data_passes", "merchant_perk_id", "merchant_offer_id"),
    ]:
        if reverse:
            op.alter_column(table, offer, new_column_name=perk)
        else:
            op.alter_column(table, perk, new_column_name=offer)


def _rename_primary_keys(reverse: bool):
    for index in [
        "merchant_{}s_pkey",
        "merchant_{}_favourites_pkey",
        "merchant_{}s_data_passes_pkey",
    ]:
        if reverse:
            op.execute(
                "alter index if exists {} rename to {}".format(
                    index.format("offer"), index.format("perk")
                )
            )
        else:
            op.execute(
                "alter index if exists {} rename to {}".format(
                    index.format("perk"), index.format("offer")
                )
            )


def _rename_constraints(reverse: bool):
    for table, perk, offer in [
        (
            "merchant_offers",
            "fk_merchants_merchant_perks",
            "fk_merchants_merchant_offers",
        ),
        (
            "merchant_offer_favourites",
            "fk_merchant_perks_merchant_perk_favourites",
            "fk_merchant_offers_merchant_offer_favourites",
        ),
        (
            "merchant_offer_favourites",
            "merchant_perk_favourites_merchant_perk_id_pda_url_key",
            "merchant_offer_favourites_merchant_offer_id_pda_url_key",
        ),
        (
            "merchant_offers_data_passes",
            "merchant_perks_data_passes_merchant_perk_id_data_pass_id_key",
            "merchant_offers_data_passes_merchant_offer_id_data_pass_id_key",
        ),
        (
            "merchant_offers_data_passes",
            "fk_merchant_perks_merchant_perks_data_passes",
            "fk_merchant_offers_merchant_offers_data_passes",
        ),
        (
            "merchant_offers_data_passes",
            "fk_data_passes_merchant_perks_data_passes",
            "fk_data_passes_merchant_offers_data_passes",
        ),
    ]:
        if reverse:
            op.execute(
                "alter table {} rename constraint {} to {}".format(table, offer, perk)
            )
        else:
            op.execute(
                "alter table {} rename constraint {} to {}".format(table, perk, offer)
            )


def upgrade() -> None:
    _rename_tables(False)
    _rename_columns(False)
    _rename_primary_keys(False)
    _rename_constraints(False)


def downgrade() -> None:
    _rename_constraints(True)
    _rename_primary_keys(True)
    _rename_columns(True)
    _rename_tables(True)
