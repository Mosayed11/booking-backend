
"""add bookings period tsrange and exclusion constraint

Revision ID: 0001_no_overlap
Revises:
Create Date: 2025-10-16
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic.
revision = '0001_no_overlap'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ensure extension for GIST index
    op.execute('CREATE EXTENSION IF NOT EXISTS btree_gist')

    # Add period computed column
    op.add_column('bookings', sa.Column('period', postgresql.TSRANGE(), nullable=True))

    # Populate existing (if any) and set NOT NULL in later migration
    op.execute("""
        UPDATE bookings
        SET period = tsrange(start_at, end_at, '[)')
        WHERE start_at IS NOT NULL AND end_at IS NOT NULL
    """)

    # Because Alembic cannot express EXCLUDE USING GIST easily, run raw SQL
    op.execute("""
        ALTER TABLE bookings
        ADD CONSTRAINT no_overlapping_bookings EXCLUDE USING GIST (
            resource_id WITH =,
            period WITH &&
        ) WHERE (status IN ('pending','confirmed'));
    """)


def downgrade():
    op.execute('ALTER TABLE bookings DROP CONSTRAINT IF EXISTS no_overlapping_bookings')
    op.drop_column('bookings', 'period')
