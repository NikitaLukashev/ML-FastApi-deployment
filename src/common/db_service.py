import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()


class DBService:

    def __init__(self, db_uri):
        """

        :param db_uri: str of database uri
        """
        self.engine = sa.create_engine(db_uri, echo=False)
        self._sessionmaker_registry = sessionmaker(autocommit=False, autoflush=True, bind=self.engine)
        self._db_session_registry = scoped_session(self._sessionmaker_registry)

    @property
    def db_session(self) -> object:
        """
        Start a registered a db session

        :rtype: object
        :return: a started and registered db session
        """
        return self._db_session_registry

    @property
    def sessionmaker(self) -> object:
        """
        Create a db session

        :rtype: object
        :return: a created db session
        """
        return self._sessionmaker_registry

    def reset_db(self) -> None:
        """
        Drop all table and recreate them without migration

        :rtype: None
        :return:  nothing
        """
        self._sessionmaker_registry.close_all()
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def close_db(self) -> None:
        """
        Close all db session

        :rtype: None
        :return:  nothing
        """
        self._sessionmaker_registry.close_all()
