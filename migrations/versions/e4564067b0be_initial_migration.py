"""Initial Migration

Revision ID: e4564067b0be
Revises: 
Create Date: 2025-01-30 16:17:07.938394

"""
import bcrypt
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e4564067b0be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('avatar', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    password = 'john1234'
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    op.execute(
        sa.text(
            "INSERT INTO users (email, password, name, avatar, created_at, updated_at)" +
            "VALUES (:email, :password, :name, :avatar, NOW(), NOW())"
        ).bindparams(
            email='johndoe@gmail.com',
            password=hash,
            name='John Doe',
            avatar='robot.png',
        )
    )


def downgrade():
    op.drop_table('users')
