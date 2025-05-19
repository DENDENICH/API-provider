"""rename column reversed on reserved in expense supplier model

Revision ID: 2a292fcf80e7
Revises: 979570fbdf25
Create Date: 2025-05-15 20:16:57.037394

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a292fcf80e7"
down_revision: Union[str, None] = "979570fbdf25"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("expense_suppliers", "reversed")
    op.add_column(
        "expense_suppliers",
        sa.Column("reserved", sa.Integer(), existing_type=sa.INTEGER(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("expense_suppliers", "reversed")
    op.add_column(
        "expense_suppliers",
        sa.Column("reserved", sa.Integer(), existing_type=sa.INTEGER(), nullable=False),
    )
