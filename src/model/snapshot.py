import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, BYTEA
from sqlalchemy.inspection import inspect

from common.db_service import Base


class Snapshot(Base):
    __tablename__ = 'snapshots'
    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    created_at = sa.Column('created_at', TIMESTAMP)
    model = sa.Column('model', BYTEA)
    couleur_mapper = sa.Column('couleur_mapper', JSONB)
    categorie_mapper = sa.Column('categorie_mapper', JSONB)
    description_produit_tfidf = sa.Column('description_produit_tfidf', BYTEA)
    nom_produit_tfidf = sa.Column('nom_produit_tfidf', BYTEA)

    def to_json(self):
        return {attribut: getattr(self, attribut) for attribut in inspect(self).attrs.keys()}
