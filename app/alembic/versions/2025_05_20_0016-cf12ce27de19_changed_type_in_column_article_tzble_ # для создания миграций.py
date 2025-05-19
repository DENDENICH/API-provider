"""changed type in column article tzble supplys on biginteger

Revision ID: cf12ce27de19
Revises: bae39e337aa5
Create Date: 2025-05-20 00:16:18.145298

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf12ce27de19"
down_revision: Union[str, None] = "bae39e337aa5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "supplys",
        "article",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "supplys",
        "article",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
