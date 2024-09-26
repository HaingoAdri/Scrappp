from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['root'] = 'root'
    
    from .routes import main
    app.register_blueprint(main)

    return app
