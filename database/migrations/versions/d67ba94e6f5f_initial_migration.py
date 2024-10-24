"""Initial migration

Revision ID: d67ba94e6f5f
Revises: 
Create Date: 2024-10-23 23:28:52.773852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'd67ba94e6f5f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get the current connection and inspector
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # List of existing tables
    tables = inspector.get_table_names()

    if 'users' not in tables:
        # Create 'users' table if it doesn't exist
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('password_hash', sa.String(length=128), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=True),
            sa.Column('is_subscribed_to_emails', sa.Boolean(), nullable=True),
            sa.Column('subscription_status', sa.String(length=20), nullable=True),
            sa.Column('subscription_start', sa.DateTime(), nullable=True),
            sa.Column('subscription_end', sa.DateTime(), nullable=True),
        )
        print("Table 'users' created.")

        # Create index on 'email' column
        op.create_index('ix_users_email', 'users', ['email'], unique=True)
        print("Index 'ix_users_email' created.")
    else:
        print("Table 'users' already exists. Skipping creation.")

        # Check existing columns
        existing_columns = [column['name'] for column in inspector.get_columns('users')]
        columns_to_add = []

        # Define all required columns
        required_columns = {
            'email': sa.Column('email', sa.String(length=120), nullable=False),
            'password_hash': sa.Column('password_hash', sa.String(length=128), nullable=False),
            'is_active': sa.Column('is_active', sa.Boolean(), nullable=True),
            'is_subscribed_to_emails': sa.Column('is_subscribed_to_emails', sa.Boolean(), nullable=True),
            'subscription_status': sa.Column('subscription_status', sa.String(length=20), nullable=True),
            'subscription_start': sa.Column('subscription_start', sa.DateTime(), nullable=True),
            'subscription_end': sa.Column('subscription_end', sa.DateTime(), nullable=True),
        }

        # Identify missing columns
        for col_name, col_def in required_columns.items():
            if col_name not in existing_columns:
                columns_to_add.append(col_def)
                print(f"Column '{col_name}' will be added.")

        # Add missing columns
        if columns_to_add:
            for column in columns_to_add:
                op.add_column('users', column)
            print("Missing columns added to 'users' table.")
        else:
            print("All required columns exist in 'users' table.")

        # Check if index exists
        existing_indexes = [index['name'] for index in inspector.get_indexes('users')]
        if 'ix_users_email' not in existing_indexes:
            op.create_index('ix_users_email', 'users', ['email'], unique=True)
            print("Index 'ix_users_email' created.")
        else:
            print("Index 'ix_users_email' already exists. Skipping creation.")


def downgrade() -> None:
    # Get the current connection and inspector
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # List of existing tables
    tables = inspector.get_table_names()

    if 'users' in tables:
        # Check if index exists before dropping
        existing_indexes = [index['name'] for index in inspector.get_indexes('users')]
        if 'ix_users_email' in existing_indexes:
            op.drop_index('ix_users_email', table_name='users')
            print("Index 'ix_users_email' dropped.")
        else:
            print("Index 'ix_users_email' does not exist. Skipping drop.")

        # Drop 'users' table
        op.drop_table('users')
        print("Table 'users' dropped.")
    else:
        print("Table 'users' does not exist. Skipping drop.")