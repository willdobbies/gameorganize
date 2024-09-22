"""fix platform row deletion & foreign key behavior on game_entry

Revision ID: be7281a4ac73
Revises: dc376f5f12cc
Create Date: 2024-09-18 18:46:31.808042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be7281a4ac73'
down_revision = 'dc376f5f12cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game_entry', schema=None) as batch_op:
        batch_op.alter_column('platform_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game_entry', schema=None) as batch_op:
        batch_op.alter_column('platform_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###