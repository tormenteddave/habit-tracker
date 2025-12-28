from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/habit_tracker_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Register blueprints
    from app.routes import categories, habits, completions, stats
    app.register_blueprint(categories.bp)
    app.register_blueprint(habits.bp)
    app.register_blueprint(completions.bp)
    app.register_blueprint(stats.bp)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
