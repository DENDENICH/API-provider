"""add user_id on users and img_path on products

Revision ID: 3efd69d85afd
Revises: 8425ce31a0e1
Create Date: 2025-03-23 23:02:11.141256

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3efd69d85afd"
down_revision: Union[str, None] = "8425ce31a0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column("users", sa.Column("user_id", sa.Integer(), nullable=False))
    op.alter_column(
        "users", "organizer_id", existing_type=sa.INTEGER(), nullable=True
    )



def downgrade() -> None:

    op.alter_column(
        "users", "organizer_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_column("users", "user_id")


