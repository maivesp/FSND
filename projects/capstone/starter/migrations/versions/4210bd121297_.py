"""empty message

Revision ID: 4210bd121297
Revises: 
Create Date: 2022-10-08 00:20:12.167651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4210bd121297'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=6), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie_cast',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.String(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_cast')
    op.drop_table('movie')
    op.drop_table('actor')
    # ### end Alembic commands ###
