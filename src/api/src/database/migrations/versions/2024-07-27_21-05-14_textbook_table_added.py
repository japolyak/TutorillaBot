"""Textbook table added

Revision ID: b4bcb7a86a24
Revises: b56eb970f789
Create Date: 2024-07-27 21:05:14.965824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4bcb7a86a24'
down_revision: Union[str, None] = 'b56eb970f789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('textbooks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('tutor_course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tutor_course_id'], ['tutor_courses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title', 'tutor_course_id', name='unique_textbook_tutor_course')
    )
    op.create_index(op.f('ix_textbooks_id'), 'textbooks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_textbooks_id'), table_name='textbooks')
    op.drop_table('textbooks')
    # ### end Alembic commands ###
