"""empty message

Revision ID: e987b2058fd5
Revises: f271b2d3a3a1
Create Date: 2020-07-27 12:02:25.736479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e987b2058fd5'
down_revision = 'f271b2d3a3a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('goal', sa.String(length=255), nullable=False),
    sa.Column('goal_ru', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers_goals',
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('teacher_id', 'goal_id')
    )
    op.drop_column('teachers', 'goals')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teachers', sa.Column('goals', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_table('teachers_goals')
    op.drop_table('goals')
    # ### end Alembic commands ###