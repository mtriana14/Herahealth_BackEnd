"""add progress entry and photo tables

Revision ID: 4f38c2a7b1d9
Revises: dd82ee2eeb86
"""

from alembic import op
import sqlalchemy as sa


revision = '4f38c2a7b1d9'
down_revision = 'dd82ee2eeb86'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    existing_tables = set(inspector.get_table_names())

    if 'progress_entries' not in existing_tables:
        op.create_table(
            'progress_entries',
            sa.Column('entry_id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('entry_date', sa.Date(), nullable=False),
            sa.Column('weight', sa.Numeric(5, 2), nullable=True),
            sa.Column('workouts_completed', sa.Integer(), nullable=True),
            sa.Column('calories_burned', sa.Integer(), nullable=True),
            sa.Column('goal_completed', sa.Boolean(), nullable=True),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('entry_id'),
        )
        op.create_index(
            'ix_progress_entries_user_date',
            'progress_entries',
            ['user_id', 'entry_date'],
            unique=False,
        )

    if 'progressphotos' not in existing_tables:
        op.create_table(
            'progressphotos',
            sa.Column('photo_id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('file_path', sa.String(length=500), nullable=False),
            sa.Column('label', sa.Enum('before', 'progress', 'after'), nullable=False),
            sa.Column('caption', sa.Text(), nullable=True),
            sa.Column('weight_at_time', sa.Numeric(5, 2), nullable=True),
            sa.Column('taken_on', sa.Date(), nullable=True),
            sa.Column('is_deleted', sa.Boolean(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('photo_id'),
        )
        op.create_index(
            'ix_progressphotos_user_deleted_date',
            'progressphotos',
            ['user_id', 'is_deleted', 'taken_on'],
            unique=False,
        )


def downgrade():
    inspector = sa.inspect(op.get_bind())
    existing_tables = set(inspector.get_table_names())

    if 'progressphotos' in existing_tables:
        op.drop_index('ix_progressphotos_user_deleted_date', table_name='progressphotos')
        op.drop_table('progressphotos')
    if 'progress_entries' in existing_tables:
        op.drop_index('ix_progress_entries_user_date', table_name='progress_entries')
        op.drop_table('progress_entries')
