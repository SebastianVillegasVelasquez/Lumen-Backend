"""seed_initial_data

Revision ID: 9ec89b245549
Revises: 62e3aa3ee6bb
Create Date: 2026-04-23 17:49:30.463382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ec89b245549'
down_revision: Union[str, Sequence[str], None] = '62e3aa3ee6bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Define the table structure for the seed
    # This is necessary because migrations don't import your models
    component_table = sa.table(
        'components',
        sa.column('component_id', sa.Integer),
        sa.column('component_name', sa.String),
        sa.column('language', sa.String)
    )

    level_table = sa.table(
        'levels',
        sa.column('level_id', sa.Integer),
        sa.column('level_name', sa.String)
    )

    # 2. Insert Components (Fontur requirements: 3 English, 2 Spanish)
    op.bulk_insert(component_table, [
        {'component_id': 1, 'component_name': 'Tourism Essentials', 'language': 'ENGLISH'},
        {'component_id': 2, 'component_name': 'Customer Service', 'language': 'ENGLISH'},
        {'component_id': 3, 'component_name': 'Guiding Techniques', 'language': 'ENGLISH'},
        {'component_id': 4, 'component_name': 'Sostenibilidad', 'language': 'SPANISH'},
        {'component_id': 5, 'component_name': 'Cultura Colombiana', 'language': 'SPANISH'},
    ])

    # 3. Insert Levels (A1 to B2)
    op.bulk_insert(level_table, [
        {'level_id': 1, 'level_name': 'A1'},
        {'level_id': 2, 'level_name': 'A2'},
        {'level_id': 3, 'level_name': 'B1'},
        {'level_id': 4, 'level_name': 'B2'},
    ])

def downgrade() -> None:
    # To revert, we delete the inserted data
    op.execute("DELETE FROM levels WHERE level_id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM components WHERE component_id IN (1, 2, 3, 4, 5)")