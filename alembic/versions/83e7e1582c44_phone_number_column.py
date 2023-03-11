"""phone number column

Revision ID: 83e7e1582c44
Revises: 4f47f9567208
Create Date: 2023-03-10 01:54:19.397737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83e7e1582c44'
down_revision = '4f47f9567208'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number')
