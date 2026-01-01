from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Database configuration
    if test_config is None:
        # Use DATABASE_URL if set (Docker), otherwise SQLite for local dev
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL',
            'sqlite:///habit_tracker.db'  # SQLite for local development
        )
    else:
        # Test configuration
        app.config.update(test_config)
    
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
