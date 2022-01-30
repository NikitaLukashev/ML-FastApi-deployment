"""create snapshots table

Revision ID: 2b0b6222482a
Revises: 
Create Date: 2022-01-29 17:10:45.432988

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSONB, BYTEA


# revision identifiers, used by Alembic.
revision = '2b0b6222482a'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'snapshots',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created_at', TIMESTAMP),
        sa.Column('model', BYTEA),
        sa.Column('couleur_mapper', JSONB),
        sa.Column('categorie_mapper', JSONB),
        sa.Column('description_produit_tfidf', BYTEA),
        sa.Column('nom_produit_tfidf', BYTEA)
    )

def downgrade():
    op.drop_table('snapshots')
