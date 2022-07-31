"""empty message

Revision ID: 50b1e1ad942c
Revises: 5f4049621507
Create Date: 2022-07-29 15:09:01.827927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50b1e1ad942c'
down_revision = '5f4049621507'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('rec_user_id_fkey', 'rec', type_='foreignkey')
    op.drop_column('rec', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rec', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('rec_user_id_fkey', 'rec', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###