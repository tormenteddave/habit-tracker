"""
Pytest configuration and fixtures for Habit Tracker tests.
"""
import pytest
from app import create_app, db
from app.models import Category, Habit, Completion
from datetime import date, timedelta


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    
    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_category(app):
    """Create a sample category for testing."""
    with app.app_context():
        category = Category(name='Health')
        db.session.add(category)
        db.session.commit()
        return {'id': category.id, 'name': category.name}


@pytest.fixture
def sample_habit(app, sample_category):
    """Create a sample habit for testing."""
    with app.app_context():
        habit = Habit(
            name='Morning Exercise',
            description='30 minutes of exercise',
            frequency='daily',
            category_id=sample_category['id']
        )
        db.session.add(habit)
        db.session.commit()
        return {'id': habit.id, 'name': habit.name}
