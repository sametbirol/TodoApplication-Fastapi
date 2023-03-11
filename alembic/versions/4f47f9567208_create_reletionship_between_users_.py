"""create reletionship between users-address tables

Revision ID: 4f47f9567208
Revises: 8cc1c67853de
Create Date: 2023-03-10 01:37:47.312434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f47f9567208'
down_revision = '8cc1c67853de'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('users',sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk',source_table="users",referent_table="address",
                          local_cols=['address_id'],remote_cols=["id"],ondelete="CASCADE")


def downgrade() :
    op.drop_constraint('address_users_fk',table_name="users")
    op.drop_column('users','address_id')
