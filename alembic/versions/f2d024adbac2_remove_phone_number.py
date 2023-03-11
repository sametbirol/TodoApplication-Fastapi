"""remove phone number 

Revision ID: f2d024adbac2
Revises: 
Create Date: 2023-03-10 01:35:03.617076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2d024adbac2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users','phone_number')


def downgrade() -> None:
    pass
