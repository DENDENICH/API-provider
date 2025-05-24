"""delete product_id from product version obj

Revision ID: ed814205d694
Revises: 47a4d75aafcc
Create Date: 2025-04-16 20:50:40.800467

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed814205d694"
down_revision: Union[str, None] = "47a4d75aafcc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_product_versions_product_id_products",
        "product_versions",
        type_="foreignkey",
    )
    op.drop_column("product_versions", "product_id")


def downgrade() -> None:
    op.add_column(
        "product_versions",
        sa.Column(
            "product_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        "fk_product_versions_product_id_products",
        "product_versions",
        "products",
        ["product_id"],
        ["id"],
    )
