"""finaly db version

Revision ID: 4f8c06feadee
Revises: 3efd69d85afd
Create Date: 2025-04-01 15:22:21.540892

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4f8c06feadee"
down_revision: Union[str, None] = "3efd69d85afd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product_versions",
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("img_path", sa.String(), nullable=True),
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
            ["product_id"],
            ["products.id"],
            name=op.f("fk_product_versions_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product_versions")),
    )
    op.create_table(
        "expense_companyss",
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("article", sa.Integer(), nullable=False),
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
            name=op.f("fk_expense_companyss_company_id_organizers"),
        ),
        sa.ForeignKeyConstraint(
            ["product_version_id"],
            ["product_versions.id"],
            name=op.f(
                "fk_expense_companyss_product_version_id_product_versions"
            ),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_expense_companyss")),
    )
    op.create_table(
        "expense_suppliers",
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("reversed", sa.Integer(), nullable=True),
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
            ["product_id"],
            ["products.id"],
            name=op.f("fk_expense_suppliers_product_id_products"),
        ),
        sa.ForeignKeyConstraint(
            ["supplier_id"],
            ["organizers.id"],
            name=op.f("fk_expense_suppliers_supplier_id_organizers"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_expense_suppliers")),
    )
    op.create_table(
        "link_codes",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.Integer(), nullable=False),
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
            ["user_id"],
            ["users.id"],
            name=op.f("fk_link_codes_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("code", "id", name=op.f("pk_link_codes")),
    )
    op.create_table(
        "user_companys",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role", sa.String(length=255), nullable=False),
        sa.Column("organizer_id", sa.Integer(), nullable=True),
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
            ["organizer_id"],
            ["organizers.id"],
            name=op.f("fk_user_companys_organizer_id_organizers"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_companys_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_companys")),
    )
    op.drop_table("expenses")
    op.add_column(
        "products",
        sa.Column("product_version_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        op.f("fk_products_product_version_id_product_versions"),
        "products",
        "product_versions",
        ["product_version_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("products", "img_path")
    op.drop_column("products", "price")
    op.drop_column("products", "description")
    op.drop_column("products", "category")
    op.drop_column("products", "name")
    op.add_column(
        "supply_products",
        sa.Column("product_version_id", sa.Integer(), nullable=False),
    )
    op.drop_constraint(
        "fk_supply_products_product_id_products",
        "supply_products",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_supply_products_product_version_id_product_versions"),
        "supply_products",
        "product_versions",
        ["product_version_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("supply_products", "product_id")
    op.add_column(
        "supplys", sa.Column("is_assembled", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "supplys", sa.Column("is_cancelled", sa.Boolean(), nullable=True)
    )
    op.drop_constraint(
        "fk_users_organizer_id_organizers", "users", type_="foreignkey"
    )
    op.drop_column("users", "user_id")
    op.drop_column("users", "role")
    op.drop_column("users", "organizer_id")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "organizer_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "role", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        "fk_users_organizer_id_organizers",
        "users",
        "organizers",
        ["organizer_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("supplys", "is_cancelled")
    op.drop_column("supplys", "is_assembled")
    op.add_column(
        "supply_products",
        sa.Column(
            "product_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(
        op.f("fk_supply_products_product_version_id_product_versions"),
        "supply_products",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_supply_products_product_id_products",
        "supply_products",
        "products",
        ["product_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("supply_products", "product_version_id")
    op.add_column(
        "products",
        sa.Column(
            "name", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "category",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "description", sa.TEXT(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "products",
        sa.Column("price", sa.NUMERIC(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "products",
        sa.Column(
            "img_path", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.drop_constraint(
        op.f("fk_products_product_version_id_product_versions"),
        "products",
        type_="foreignkey",
    )
    op.drop_column("products", "product_version_id")
    op.create_table(
        "expenses",
        sa.Column(
            "organizer_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "product_id", sa.INTEGER(), autoincrement=False, nullable=False
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
            ["organizer_id"],
            ["organizers.id"],
            name="fk_expenses_organizer_id_organizers",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name="fk_expenses_product_id_products",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_expenses"),
    )
    op.drop_table("user_companys")
    op.drop_table("link_codes")
    op.drop_table("expense_suppliers")
    op.drop_table("expense_companyss")
    op.drop_table("product_versions")
