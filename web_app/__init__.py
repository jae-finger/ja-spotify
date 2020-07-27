from flask import Flask
from web_app.routes.api_routes import api_routes

def create_app():
    """Instantiate Flask API."""
    app = Flask(__name__)

    app.register_blueprint(api_routes)

    return app

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)
