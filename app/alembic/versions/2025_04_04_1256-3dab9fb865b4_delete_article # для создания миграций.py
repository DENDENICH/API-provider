"""delete article

Revision ID: 3dab9fb865b4
Revises: 4f8c06feadee
Create Date: 2025-04-04 12:56:02.347962

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3dab9fb865b4"
down_revision: Union[str, None] = "4f8c06feadee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("expense_companyss", "article")


def downgrade() -> None:
    op.add_column(
        "expense_companyss",
        sa.Column(
            "article", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
