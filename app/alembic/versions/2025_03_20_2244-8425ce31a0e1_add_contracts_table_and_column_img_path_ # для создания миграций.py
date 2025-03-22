"""add contracts table and column 'img_path' in products

Revision ID: 8425ce31a0e1
Revises: 18d3f38bf79e
Create Date: 2025-03-20 22:44:03.070333

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8425ce31a0e1"
down_revision: Union[str, None] = "18d3f38bf79e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contracts",
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["organizers.id"],
            name=op.f("fk_contracts_company_id_organizers"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["supplier_id"],
            ["organizers.id"],
            name=op.f("fk_contracts_supplier_id_organizers"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contracts")),
    )
    op.add_column(
        "products", sa.Column("article", sa.Integer(), nullable=False)
    )
    op.add_column(
        "products", sa.Column("img_path", sa.String(), nullable=True)
    )
    op.create_unique_constraint(
        op.f("uq_products_article"), "products", ["article"]
    )
    op.add_column(
        "supplys", sa.Column("article", sa.Integer(), nullable=False)
    )
    op.create_unique_constraint(
        op.f("uq_supplys_article"), "supplys", ["article"]
    )
    op.alter_column(
        "users", "phone", existing_type=sa.VARCHAR(length=255), nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        "users", "phone", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    op.drop_constraint(op.f("uq_supplys_article"), "supplys", type_="unique")
    op.drop_column("supplys", "article")
    op.drop_constraint(op.f("uq_products_article"), "products", type_="unique")
    op.drop_column("products", "img_path")
    op.drop_column("products", "article")
    op.drop_table("contracts")
