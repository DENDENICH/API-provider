"""changed column in supplys

Revision ID: bae39e337aa5
Revises: 2a292fcf80e7
Create Date: 2025-05-20 00:07:46.687505

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bae39e337aa5"
down_revision: Union[str, None] = "2a292fcf80e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("supplys", "is_assembled")
    op.drop_column("supplys", "is_cancelled")
    op.add_column(
        "supplys",
        sa.Column("is_wait_confirm", sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("supplys", "is_assembled")
    op.drop_column("supplys", "is_cancelled")
    op.add_column(
        "supplys",
        sa.Column("is_wait_confirm", sa.Boolean(), nullable=False),
    )
