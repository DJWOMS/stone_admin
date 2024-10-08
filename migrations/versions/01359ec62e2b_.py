"""empty message

Revision ID: 01359ec62e2b
Revises: 18750b53a4e1
Create Date: 2024-07-07 16:22:11.168724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01359ec62e2b'
down_revision = '18750b53a4e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prices')
    # ### end Alembic commands ###
