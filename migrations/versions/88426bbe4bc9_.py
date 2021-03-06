"""empty message

Revision ID: 88426bbe4bc9
Revises: 71ff390537fc
Create Date: 2018-04-17 20:53:02.785538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88426bbe4bc9'
down_revision = '71ff390537fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('logtype', sa.String(length=20), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    # ### end Alembic commands ###
