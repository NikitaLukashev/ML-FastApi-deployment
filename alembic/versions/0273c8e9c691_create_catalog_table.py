"""create catalog table

Revision ID: 0273c8e9c691
Revises: f1c7c79dac4a
Create Date: 2022-01-29 18:08:43.663917

"""
from alembic import op
import sqlalchemy as sa
import pandas as pd
from src.model.catalog import Catalog
from src.common.config import CONFIG

# revision identifiers, used by Alembic.
revision = '0273c8e9c691'
down_revision = 'f1c7c79dac4a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'catalog',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nb_images', sa.Float),
        sa.Column('longueur_image', sa.Float),
        sa.Column('largeur_image', sa.Float),
        sa.Column('description_produit', sa.String),
        sa.Column('annee', sa.Float),
        sa.Column('couleur', sa.String),
        sa.Column('prix', sa.Float),
        sa.Column('categorie', sa.String),
        sa.Column('nom_produit', sa.String),
        sa.Column('delai_vente', sa.Integer)
    )

    insert_catalogs(CONFIG['CATALOG_DATA'])


def insert_catalogs(file_name):
    df = pd.read_csv(file_name)
    catalog_records = df.to_dict('records')
    op.bulk_insert(Catalog.__table__, catalog_records)




def downgrade():
    op.drop_table('catalog')

