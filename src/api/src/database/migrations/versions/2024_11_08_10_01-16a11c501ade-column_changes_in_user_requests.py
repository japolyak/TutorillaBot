"""column changes in user requests

Revision ID: 16a11c501ade
Revises: d8c3d44824a3
Create Date: 2024-11-08 10:01:56.923032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '16a11c501ade'
down_revision: Union[str, None] = 'd8c3d44824a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_requests', sa.Column('request_time_unix', sa.BigInteger(), server_default='0', nullable=False), schema='core')
    op.add_column('users_requests', sa.Column('role', sa.Integer(), server_default='0', nullable=False), schema='core')
    op.execute("""
                UPDATE core.users_requests
                SET request_time_unix = (EXTRACT(EPOCH FROM request_datetime) * 1000)::BIGINT,
                    role = CASE WHEN tutor_role THEN 1 ELSE 2 END;
            """)
    op.drop_column('users_requests', 'tutor_role', schema='core')
    op.drop_column('users_requests', 'request_datetime', schema='core')
    op.drop_column('users_requests', 'student_role', schema='core')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_requests', sa.Column('student_role', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False), schema='core')
    op.add_column('users_requests', sa.Column('request_datetime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False), schema='core')
    op.add_column('users_requests', sa.Column('tutor_role', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False), schema='core')
    op.execute("""
                UPDATE core.users_requests
                SET request_datetime = to_timestamp(request_time_unix / 1000),
                    tutor_role = CASE WHEN role = 1 THEN true ELSE false END,
                    student_role = CASE WHEN role = 2 THEN true ELSE false END;
            """)
    op.drop_column('users_requests', 'role', schema='core')
    op.drop_column('users_requests', 'request_time_unix', schema='core')
    # ### end Alembic commands ###
