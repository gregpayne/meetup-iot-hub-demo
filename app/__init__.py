import os
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=False):
    # create and configure the app
    app = Flask(__name__)
    app.debug = debug
    app.config['TABLE_CONNECTION_STRING'] = os.environ["TABLE_CONNECTION_STRING"]
    # if app.config['TABLE_CONNECTION_STRING'] is None:
        # raise ValueError("No TABLE_CONNECTION_STRING set for Flask application")

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!!'
    
    from . import main
    app.register_blueprint(main.bp)

    socketio.init_app(app)
    return app
