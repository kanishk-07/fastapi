"""create posts table

Revision ID: 94ee27699c1b
Revises: 
Create Date: 2023-05-07 14:22:10.732130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94ee27699c1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False, primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
