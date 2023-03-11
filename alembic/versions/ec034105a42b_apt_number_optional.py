"""apt number optional

Revision ID: ec034105a42b
Revises: 83e7e1582c44
Create Date: 2023-03-10 10:59:15.463211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec034105a42b'
down_revision = '83e7e1582c44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address',sa.Column('apt_num',sa.String,nullable=True))

def downgrade() -> None:
    op.drop_column('address','apt_num')
