from common.config import CONFIG
from common.db_service import DBService
from common.logger import logger
from manager.manager import Manager
from model.snapshot import Snapshot
from model.prediction import Prediction
from fixture import prediction_fixture
db_service = DBService(CONFIG['DATABASE'])
db_session = db_service.db_session


def test_manager_create_initial_model_if_no_model(mocker):
    logger.info('Instanciate manager without trained model.'
                ' An ml algorithm is trained and his snapshot is inserted into the empty '
                'db with an id equals to 1')

    db_service.reset_db()
    engine = db_service.engine

    manager = Manager(db_session, engine, logger)

    assert db_session.query(Snapshot).count() == 1
    assert db_session.query(Snapshot.id).first()[0] == 1


def test_manager_take_initial_model_if_present(mocker):
    logger.info('Instanciate manager without trained model.'
                ' An ml algorithm is trained and his snapshot is inserted into the db with an id equals to 1.'
                'Instanciate a second manager, it will take the trained model by previous without'
                ' retrain.')

    db_service.reset_db()
    engine = db_service.engine

    manager_1 = Manager(db_session, engine, logger)
    manager_2 = Manager(db_session, engine, logger)

    last_state = manager_2.algorithm_id

    assert db_session.query(Snapshot.id).order_by(Snapshot.id.desc()).first()[0] == last_state
    assert db_session.query(Snapshot).count() == 1
    assert db_session.query(Snapshot.id).first()[0] == 1


def test_manager_train(mocker):
    logger.info('Instanciate manager without trained model.'
                ' An ml algorithm is trained and his snapshot is inserted into the db with an id equals to 1.'
                'Train the algorithm, it will insert a new snapshot of the algorithm into the db with a new id 2')
    db_service.reset_db()
    engine = db_service.engine

    manager_1 = Manager(db_session, engine, logger)
    manager_1.train()

    assert db_session.query(Snapshot).count() == 2
    assert db_session.query(Snapshot.id).order_by(Snapshot.id.desc()).first()[0] == 2


def test_manager_predict(mocker):
    logger.info('Instanciate manager.'
                ' Predict on a fixture of input. '
                'Algorythm insert prediction into the db table predictions.'
                'Predicted output is of type dictionary with key as 0, 1, 2 '
                'and values as probability for each classes with sum equals to 1')

    db_service.reset_db()
    engine = db_service.engine

    manager = Manager(db_session, engine, logger)
    intial_number_prediction = db_session.query(Prediction.id).count()
    manager.predict(prediction_fixture)

    assert db_session.query(Prediction.id).count() == intial_number_prediction + 1
    assert isinstance(db_session.query(Prediction.prediction).order_by(Prediction.id.desc()).first()[0], dict)
    assert set(db_session.query(Prediction.prediction).order_by(Prediction.id.desc()).first()[0].keys()) == {'0', '1', '2'}
    assert sum(db_session.query(Prediction.prediction).order_by(Prediction.id.desc()).first()[0].values()) == 1


def test_manager_get_state(mocker):
    logger.info('Instanciate manager, it will take the last model in the db'
                ' or retrain one if there isn t.'
                'Retrieve the last state from the manager algorithm and the db. They should be equal'
               )

    db_service.reset_db()
    engine = db_service.engine

    manager = Manager(db_session, engine, logger)
    intial_state = manager.algorithm_id

    assert db_session.query(Snapshot.id).order_by(Snapshot.id.desc()).first()[0] == intial_state

