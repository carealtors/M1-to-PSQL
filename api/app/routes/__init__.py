from dotenv import load_dotenv
def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Register blueprints
    from .routes.summary import summary_blueprint
    from .routes.banks import banks_blueprint
    from .routes.invoices import invoices_blueprint
    from .routes.efts import efts_blueprint
    from .routes.chargebacks import chargebacks_blueprint
    from .routes.dues import dues_blueprint

    app.register_blueprint(summary_blueprint)
    app.register_blueprint(banks_blueprint)
    app.register_blueprint(invoices_blueprint)
    app.register_blueprint(efts_blueprint)
    app.register_blueprint(chargebacks_blueprint)
    app.register_blueprint(dues_blueprint)

    return app
