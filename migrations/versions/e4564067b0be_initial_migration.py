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
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password', sa.LargeBinary(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('avatar', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    password = 'john1234'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    op.execute(
        sa.text(
            "INSERT INTO users (email, password, name, avatar, created_at, updated_at) "
            "VALUES (:email, :password, :name, :avatar, NOW(), NOW())"
        ).bindparams(
            email='johndoe@gmail.com',
            password=hashed_password,
            name='John Doe',
            avatar='robot.png',
        )
    )


def downgrade():
    op.drop_table('users')
