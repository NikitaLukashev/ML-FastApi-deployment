"""create predictions table

Revision ID: f1c7c79dac4a
Revises: 2b0b6222482a
Create Date: 2022-01-29 17:15:38.665866

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP


# revision identifiers, used by Alembic.
revision = 'f1c7c79dac4a'
down_revision = '2b0b6222482a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'predictions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created_at', TIMESTAMP),
        sa.Column('input', JSONB),
        sa.Column('prediction', JSONB),
        sa.Column('model_id', sa.Integer)

    )

def downgrade():
    op.drop_table('predictions')

