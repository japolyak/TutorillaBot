"""Private courses table column renamed

Revision ID: e8ff86ab2620
Revises: b4bcb7a86a24
Create Date: 2024-07-29 21:11:45.053249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8ff86ab2620'
down_revision: Union[str, None] = 'b4bcb7a86a24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('unique_student_course', 'private_courses', type_='unique', schema='core')
    op.drop_constraint('private_courses_course_id_fkey', 'private_courses', type_='foreignkey', schema='core')

    op.alter_column('private_courses', 'course_id', new_column_name='tutor_course_id', schema='core')

    op.create_unique_constraint('unique_student_course', 'private_courses', ['student_id', 'tutor_course_id'], schema='core')
    op.create_foreign_key('private_courses_tutor_course_id_fkey', 'private_courses', 'tutor_courses',
                          ['tutor_course_id'], ['id'], source_schema='core', referent_schema='core')


def downgrade() -> None:
    op.drop_constraint('unique_student_course', 'private_courses', type_='unique', schema='core')
    op.drop_constraint('private_courses_tutor_course_id_fkey', 'private_courses', type_='foreignkey', schema='core')

    op.alter_column('private_courses', 'tutor_course_id', new_column_name='course_id', schema='core')

    op.create_unique_constraint('unique_student_course', 'private_courses', ['student_id', 'course_id'], schema='core')
    op.create_foreign_key('private_courses_course_id_fkey', 'core.private_courses', 'core.tutor_courses',
                          ['course_id'], ['id'], source_schema='core', referent_schema='core')
