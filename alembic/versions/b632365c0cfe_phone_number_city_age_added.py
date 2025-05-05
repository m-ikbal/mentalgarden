"""phone number, city, age added

Revision ID: b632365c0cfe
Revises: 489853755007
Create Date: 2025-05-05 13:41:53.718595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b632365c0cfe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('city', sa.String(), nullable=True))
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))


def downgrade() -> None:
    pass
