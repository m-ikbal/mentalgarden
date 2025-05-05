"""TreeSatate table added

Revision ID: a62454e73288
Revises: b632365c0cfe
Create Date: 2025-05-05 14:16:02.964247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a62454e73288'
down_revision: Union[str, None] = 'b632365c0cfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tree_states', sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
                    sa.Column('date', sa.Date, default=sa.func.current_date()),
                    sa.Column('emotion', sa.String),
                    sa.Column('leaf_color', sa.String),
                    sa.Column('has_flowers', sa.Boolean, default=False),
                    sa.Column('falling_leaves', sa.Boolean, default=False),
                    )


def downgrade() -> None:
    pass
