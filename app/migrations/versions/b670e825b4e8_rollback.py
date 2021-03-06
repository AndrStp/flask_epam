"""Rollback

Revision ID: b670e825b4e8
Revises: 80d9145e97e5
Create Date: 2021-12-09 11:08:23.468488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b670e825b4e8'
down_revision = '80d9145e97e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user-course', 'date_enrolled')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user-course', sa.Column('date_enrolled', sa.DATE(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
