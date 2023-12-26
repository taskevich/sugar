"""new column my_erp_id

Revision ID: f5306a1d661f
Revises: 75630d207b98
Create Date: 2023-10-24 17:01:48.868977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5306a1d661f'
down_revision = '75630d207b98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("quests", sa.Column("my_erp_id", sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column("quests", "my_erp_id")
