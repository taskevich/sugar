"""new table and column

Revision ID: 75630d207b98
Revises: dc125edaad6f
Create Date: 2023-10-17 15:16:46.693495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75630d207b98'
down_revision = 'dc125edaad6f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gallery",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("quest_id", sa.Integer, nullable=True),
        sa.Column("photo", sa.Text)
    )
    op.create_foreign_key("fk_gallery_to_quest_id", "gallery", "quests", ["quest_id"], ["id"])


def downgrade() -> None:
    op.drop_table("gallery")
