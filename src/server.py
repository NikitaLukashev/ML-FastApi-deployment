from logging import Logger

from flask import Flask, request, jsonify, Response
from werkzeug.exceptions import HTTPException, default_exceptions

from manager import Manager


class Server:
    def __init__(self, manager: Manager, logger: Logger):
        """
        The server depending on the manager and the custom logger

        :param manager: Manager which manage training prediction and model state
        :param logger: Logger which format logs
        """
        self.flask = Flask(__name__)

        logger.info("Initializing server...")

        self.manager = manager
        self.logger = logger

        self.flask.add_url_rule('/train', 'train', self.train, methods=['POST'])
        self.flask.add_url_rule('/predict', 'predict', self.predict, methods=['POST'])
        self.flask.add_url_rule('/state', 'get_state', self.get_state, methods=['GET'])
        self.flask.teardown_request(manager.teardown)
        # For returning exception message as json
        for ex in default_exceptions:
            self.flask.register_error_handler(ex, self.error_handler)

    def start(self, port: int) -> None:
        """
        Starting the server
        :param port: int to specify the port
        """
        self.logger.info(f'Starting server on port {port}...')
        self.flask.run(debug=True, port=port, host='0.0.0.0')

    def test(self) -> object:
        """
        Testing the server
        """
        self.flask.config['TESTING'] = True
        return self.flask.test_client()

    def train(self) -> (Response, int):
        """
        Train the model
        """
        resource = self.manager.train()
        self.logger.info(f'Training new model {resource["id"]} on full dataset the {resource["created_at"]}')
        return jsonify([resource]), 200

    def predict(self) -> (Response, int):
        """
        Predict on the incoming payload
        :return: a Response with score for each class and an http number
        """
        payload = request.get_json()
        resource = self.manager.predict(payload)
        self.logger.info(f'New predicted resource {resource} created')
        return jsonify(resource), 200

    def get_state(self) -> (Response, int):
        """
        Retrieve last trained model state
        :return: a Response with model state and an http number
        """
        self.logger.info('Retrieving internal algorithm state')
        res = self.manager.get_state()
        return jsonify(res), 200

    def error_handler(self, exception: Exception):
        self.logger.exception('')
        code = 500
        if isinstance(exception, NameError):
            code = 400
        if isinstance(exception, HTTPException):
            code = exception.code
        response = jsonify(message=str(exception)), code
        return response
