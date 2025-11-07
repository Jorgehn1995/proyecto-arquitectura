"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-11-07

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('rfid_tag', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('rfid_tag')
    )
    
    # Create reads table
    op.create_table('reads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create access table
    op.create_table('access',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create pumps table
    op.create_table('pumps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('read_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('status', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['read_id'], ['reads.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('read_id')
    )
    
    # Create sensors table
    op.create_table('sensors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('read_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('humidity', sa.Float(), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['read_id'], ['reads.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('read_id')
    )
    
    # Create fans table
    op.create_table('fans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('read_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('status', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['read_id'], ['reads.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('read_id')
    )


def downgrade():
    op.drop_table('fans')
    op.drop_table('sensors')
    op.drop_table('pumps')
    op.drop_table('access')
    op.drop_table('reads')
    op.drop_table('users')
