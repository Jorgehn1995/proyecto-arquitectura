"""remove names and add smoke table

Revision ID: 003
Revises: 002
Create Date: 2025-11-07

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Create smokes table
    op.create_table(
        'smokes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('read_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['read_id'], ['reads.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('read_id')
    )
    
    # Remove name columns from pumps, sensors, and fans
    op.drop_column('pumps', 'name')
    op.drop_column('sensors', 'name')
    op.drop_column('fans', 'name')


def downgrade():
    # Add name columns back
    op.add_column('pumps', sa.Column('name', sa.String(length=200), nullable=False, server_default='Pump'))
    op.add_column('sensors', sa.Column('name', sa.String(length=200), nullable=False, server_default='Sensor'))
    op.add_column('fans', sa.Column('name', sa.String(length=200), nullable=False, server_default='Fan'))
    
    # Remove server_default after adding
    op.alter_column('pumps', 'name', server_default=None)
    op.alter_column('sensors', 'name', server_default=None)
    op.alter_column('fans', 'name', server_default=None)
    
    # Drop smokes table
    op.drop_table('smokes')
