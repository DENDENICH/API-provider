"""change column integer on bigint for article in products

Revision ID: 22ae89e147e1
Revises: 5ad45d2bcc4d
Create Date: 2025-04-21 02:40:44.934519

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "22ae89e147e1"
down_revision: Union[str, None] = "5ad45d2bcc4d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "products",
        "article",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "products",
        "article",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
