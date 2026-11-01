from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    if app.config['DATA_BACKEND'] != 'mock':
        raise RuntimeError('Oracle adapter is not implemented yet; use DATA_BACKEND=mock.')

    @app.get('/')
    def home():
        return 'CareerPulse — fictional demo scaffold'

    return app


if __name__ == '__main__':
    create_app().run()
