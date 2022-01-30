from common.config import CONFIG
from common.db_service import DBService
from common.logger import logger
from manager.manager import Manager
from server import Server

if __name__ == '__main__':
    db_service = DBService(CONFIG['DATABASE'])
    db_session = db_service.db_session
    engine = db_service.engine

    manager = Manager(db_session, engine, logger)
    server = Server(manager, logger)

    server.start(port=CONFIG['PORT'])
