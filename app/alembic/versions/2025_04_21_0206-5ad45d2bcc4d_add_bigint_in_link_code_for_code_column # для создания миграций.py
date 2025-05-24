"""add bigint in link_code for code column

Revision ID: 5ad45d2bcc4d
Revises: ed814205d694
Create Date: 2025-04-21 02:06:47.015763

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5ad45d2bcc4d"
down_revision: Union[str, None] = "ed814205d694"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "link_codes",
        "code",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.add_column(
        "product_versions", sa.Column("description", sa.Text(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("product_versions", "description")
    op.alter_column(
        "link_codes",
        "code",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
