# backend/app.py
from flask import Flask
from flask_cors import CORS
from .database import engine, Base
from .routes import bp as api_bp

def create_app():
    app = Flask(__name__, static_folder=None)
    CORS(app)
    app.register_blueprint(api_bp)
    Base.metadata.create_all(bind=engine)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
