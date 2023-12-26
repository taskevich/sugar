"""new column gallery

Revision ID: bccc6953f406
Revises: f5306a1d661f
Create Date: 2023-11-14 08:28:40.546841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bccc6953f406'
down_revision = 'f5306a1d661f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("gallery", sa.Column("is_main", sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column("gallery", "is_main")
