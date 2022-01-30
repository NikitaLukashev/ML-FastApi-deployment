import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.inspection import inspect

from src.common.db_service import Base


class Snapshot(Base):
    __tablename__ = 'snapshots'
    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    created_at = sa.Column('created_at', TIMESTAMP)
    model = sa.Column('model', JSONB)
    couleur_mapper = sa.Column('couleur_mapper', JSONB)
    categorie_mapper = sa.Column('categorie_mapper', JSONB)


def to_json(self):
        return {attribut: getattr(self, attribut) for attribut in inspect(self).attrs.keys()}
