import sqlalchemy as sa
from sqlalchemy.inspection import inspect

from common.db_service import Base


class Catalog(Base):
    __tablename__ = 'catalog'

    id = sa.Column('id', sa.Integer, primary_key=True)
    nb_images = sa.Column('nb_images', sa.Float)
    longueur_image = sa.Column('longueur_image', sa.Float)
    largeur_image = sa.Column('largeur_image', sa.Float)
    description_produit = sa.Column('description_produit', sa.String)
    annee = sa.Column('annee', sa.Float)
    couleur = sa.Column('couleur', sa.String)
    prix = sa.Column('prix', sa.Float)
    categorie = sa.Column('categorie', sa.String)
    nom_produit = sa.Column('nom_produit', sa.String)
    delai_vente = sa.Column('delai_vente', sa.Integer)

    def to_json(self):
        return {attribut: getattr(self, attribut) for attribut in inspect(self).attrs.keys()}
