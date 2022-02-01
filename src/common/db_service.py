import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()


class DBService:

    def __init__(self, db_uri):
        self.engine = sa.create_engine(db_uri, echo=False)
        self._sessionmaker_registry = sessionmaker(autocommit=False, autoflush=True, bind=self.engine)
        self._db_session_registry = scoped_session(self._sessionmaker_registry)

    @property
    def db_session(self):
        return self._db_session_registry

    @property
    def sessionmaker(self):
        return self._sessionmaker_registry

    def reset_db(self):
        self._sessionmaker_registry.close_all()
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def close_db(self):
        self._sessionmaker_registry.close_all()
