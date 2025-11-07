"""Add thresholds table

Revision ID: 002
Revises: 001
Create Date: 2025-11-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    """Create thresholds table."""
    op.create_table(
        'thresholds',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('min_humidity', sa.Float(), nullable=False),
        sa.Column('max_humidity', sa.Float(), nullable=False),
        sa.Column('min_temperature', sa.Float(), nullable=False),
        sa.Column('max_temperature', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    """Drop thresholds table."""
    op.drop_table('thresholds')
