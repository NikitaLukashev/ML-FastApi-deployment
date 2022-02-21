from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

from model.snapshot import Snapshot
from model.prediction import Prediction
from controller.processor import Processor


class Manager:
    def __init__(self, db_session, engine, logger):
        # self, algorithm, snapshot_provider, db_session, logger
        # By default we try to pick an existing ml model from db, if there is not one
        # we instantiate a raw model

        self.db_session = db_session
        self.engine = engine
        self.logger = logger
        self.algorithm = None
        self.algorithm_id = 0
        self._load_snapshot_if_exists()

    def _load_snapshot_if_exists(self) -> None:
        """
        Load an existing model from the db if db contains one
        :return: None
        """
        snapshot = self.db_session.query(Snapshot).order_by(Snapshot.created_at.desc()).first()
        self.logger.info('Checking for a pretrained ml model into db')
        if snapshot is not None:
            self.algorithm = pickle.loads(snapshot.model)
            self.algorithm_id = snapshot.id
            self.logger.info('Loading most recent trained ml model from db')
        else:
            self.train()
            self.algorithm_id = self.db_session.query(Snapshot.id).first()[0]
            self.logger.info('Training raw ml model on full dataset')

    def predict(self, payload) -> dict:
        """
        Predict on the incoming payload
        :return: dict with score for each class
        """
        self.logger.info('Predicting on new resource')

        created_at = datetime.now()

        couleur_mapper = self.db_session.query(Snapshot.couleur_mapper). \
            where(Snapshot.id == self.algorithm_id).first()[0]

        categorie_mapper = self.db_session.query(Snapshot.categorie_mapper). \
            where(Snapshot.id == self.algorithm_id).first()[0]

        description_produit_tfidf = pickle.loads(self.db_session.
                                                 query(Snapshot.description_produit_tfidf).
                                                 where(Snapshot.id == self.algorithm_id).
                                                 first()[0])

        nom_produit_tfidf = pickle.loads(self.db_session.
                                         query(Snapshot.nom_produit_tfidf).
                                         where(Snapshot.id == self.algorithm_id).
                                         first()[0])

        resource = Processor.process_predict(payload, couleur_mapper, categorie_mapper, description_produit_tfidf,
                                             nom_produit_tfidf)
        clf = self.algorithm
        res = clf.predict_proba(resource)
        res_json = {'0': res[0, 0], '1': res[0, 1], '2': res[0, 2]}
        prediction = Prediction(created_at=created_at, input=payload,
                                prediction=res_json, model_id=self.algorithm_id)

        self.db_session.add(prediction)
        self.db_session.commit()

        return res_json

    def train(self) -> dict:
        """
        Train the ml model on the incoming payload
        :return: a dict with id of the trained model and the date of training
        """
        self.logger.info('Training model on full dataset')

        query = '''select * from catalog'''
        df = pd.read_sql_query(query, self.engine)
        x, y, categorical_mapper, description_produit_tfidf, nom_produit_tfidf = Processor.process_train(df)
        clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=1)
        clf = clf.fit(x, y)
        snap = pickle.dumps(clf)
        description_produit_tfidf_snap = pickle.dumps(description_produit_tfidf)
        nom_produit_tfidf_snap = pickle.dumps(nom_produit_tfidf)

        created_at = datetime.now()
        snapshot = Snapshot(created_at=created_at,
                            model=snap,
                            couleur_mapper=categorical_mapper['couleur'],
                            categorie_mapper=categorical_mapper['categorie'],
                            description_produit_tfidf=description_produit_tfidf_snap,
                            nom_produit_tfidf=nom_produit_tfidf_snap
                            )
        self.db_session.add(snapshot)
        self.db_session.commit()
        self.algorithm_id += 1
        self.algorithm = clf
        return {'id': snapshot.id, 'created_at': snapshot.created_at}

    def get_state(self) -> str:
        """
        Retrieve the internal state of the last model

        :return: a string with the algorythm version
        """
        self.logger.info('Retrieving current model id')
        return f'algorythm version {self.algorithm_id}'

    def teardown(self, exception: Exception = None):
        """
        Remove the current session attached to the request thread to avoid connection hanging.
        """
        if exception:
            self.db_session.rollback()
        else:
            self.db_session.commit()
        self.db_session.remove()
