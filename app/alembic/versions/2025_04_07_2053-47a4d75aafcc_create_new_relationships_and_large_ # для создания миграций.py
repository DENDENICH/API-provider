"""create new relationships and large_binary type for password

Revision ID: 47a4d75aafcc
Revises: 3dab9fb865b4
Create Date: 2025-04-07 20:53:06.478554

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "47a4d75aafcc"
down_revision: Union[str, None] = "3dab9fb865b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "expense_companys",
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("product_version_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
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
            name=op.f("fk_expense_companys_company_id_organizers"),
        ),
        sa.ForeignKeyConstraint(
            ["product_version_id"],
            ["product_versions.id"],
            name=op.f(
                "fk_expense_companys_product_version_id_product_versions"
            ),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_expense_companys")),
    )
    op.drop_table("expense_companyss")
    op.alter_column(
        "users",
        "password",
        existing_type=sa.VARCHAR(),
        type_=sa.LargeBinary(),
        existing_nullable=False,
        postgresql_using="password::bytea"
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "password",
        existing_type=sa.LargeBinary(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="password::bytea"
    )
    op.create_table(
        "expense_companyss",
        sa.Column(
            "company_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "product_version_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "quantity", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["organizers.id"],
            name="fk_expense_companyss_company_id_organizers",
        ),
        sa.ForeignKeyConstraint(
            ["product_version_id"],
            ["product_versions.id"],
            name="fk_expense_companyss_product_version_id_product_versions",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_expense_companyss"),
    )
    op.drop_table("expense_companys")
