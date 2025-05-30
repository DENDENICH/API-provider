"""add default value in column reserve in table expense_supplier

Revision ID: 979570fbdf25
Revises: 22ae89e147e1
Create Date: 2025-05-07 00:18:48.310044

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "979570fbdf25"
down_revision: Union[str, None] = "b6078e83cd5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "expense_suppliers",
        "reversed",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

def downgrade() -> None:
    op.alter_column(
        "expense_suppliers",
        "reversed",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
