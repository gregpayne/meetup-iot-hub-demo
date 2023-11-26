import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)


def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

        # ensure the instance and scripts folders exists
    try:
        try:
            os.makedirs(app.instance_path)
        except:
            pass
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!!'
    
    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    return app
