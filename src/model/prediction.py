import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.inspection import inspect

from src.common.db_service import Base


class Prediction(Base):
    __tablename__ = 'predictions'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    created_at = sa.Column('created_at', TIMESTAMP)
    input = sa.Column('input', JSONB)
    prediction = sa.Column('prediction', JSONB)
    model_id = sa.Column('model_id', sa.Integer)

    def to_json(self):
        return {attribut: getattr(self, attribut) for attribut in inspect(self).attrs.keys()}
