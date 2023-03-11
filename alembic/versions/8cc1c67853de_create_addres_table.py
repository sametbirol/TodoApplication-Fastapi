"""create addres table

Revision ID: 8cc1c67853de
Revises: f2d024adbac2
Create Date: 2023-03-10 01:36:16.815105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cc1c67853de'
down_revision = 'f2d024adbac2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id',sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('address1',sa.String(), nullable=False),
                    sa.Column('address2',sa.String(), nullable=False),
                    sa.Column('city',sa.String(), nullable=False),
                    sa.Column('state',sa.String(), nullable=False),
                    sa.Column('country',sa.String(), nullable=False),
                    sa.Column('postalcode',sa.String(), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('address')
