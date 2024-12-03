from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    # Load environment variables
    load_dotenv()

    # Create Flask app
    app = Flask(__name__)

    # Configure app
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .routes.summary import summary_blueprint
    from .routes.banks import banks_blueprint
    from .routes.invoices import invoices_blueprint
    from .routes.efts import efts_blueprint
    from .routes.chargebacks import chargebacks_blueprint
    from .routes.banks import banks_blueprint


    app.register_blueprint(banks_blueprint, url_prefix="/banks")
    app.register_blueprint(summary_blueprint, url_prefix="/summary")
    app.register_blueprint(invoices_blueprint, url_prefix="/invoices")
    app.register_blueprint(efts_blueprint, url_prefix="/efts")
    app.register_blueprint(chargebacks_blueprint, url_prefix="/chargebacks")

    return app
