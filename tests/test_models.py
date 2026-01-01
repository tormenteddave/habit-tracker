"""
Unit tests for database models.
"""
from app import db
from app.models import Habit, Completion
from datetime import date, timedelta


def test_habit_streak_calculation(app):
    """Test that streak calculation works for consecutive days."""
    with app.app_context():
        habit = Habit(name='Daily Habit', frequency='daily')
        db.session.add(habit)
        db.session.commit()
        
        # Add 5 consecutive days of completions
        today = date.today()
        for i in range(5):
            completion = Completion(
                habit_id=habit.id,
                completed_date=today - timedelta(days=i)
            )
            db.session.add(completion)
        db.session.commit()
        
        assert habit.calculate_streak() == 5


def test_habit_streak_with_gap(app):
    """Test that streak resets when there's a gap in completions."""
    with app.app_context():
        habit = Habit(name='Daily Habit', frequency='daily')
        db.session.add(habit)
        db.session.commit()
        
        today = date.today()
        # Complete today and yesterday only
        for i in range(2):
            completion = Completion(
                habit_id=habit.id,
                completed_date=today - timedelta(days=i)
            )
            db.session.add(completion)
        
        # Skip day 2, add older completions (shouldn't count)
        for i in range(4, 6):
            completion = Completion(
                habit_id=habit.id,
                completed_date=today - timedelta(days=i)
            )
            db.session.add(completion)
        db.session.commit()
        
        # Streak should only be 2
        assert habit.calculate_streak() == 2
