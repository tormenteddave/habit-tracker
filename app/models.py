from app import db
from datetime import datetime, date, timedelta

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relationship
    habits = db.relationship('Habit', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Habit(db.Model):
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(10), nullable=False)  # 'daily' or 'weekly'
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship
    completions = db.relationship('Completion', backref='habit', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.CheckConstraint(frequency.in_(['daily', 'weekly']), name='check_frequency'),
    )
    
    def to_dict(self, include_streak=False):
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'frequency': self.frequency,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
        if include_streak:
            result['current_streak'] = self.calculate_streak()
        return result
    
    def calculate_streak(self):
        """Calculate the current streak for this habit."""
        today = date.today()
        completion_dates = sorted(
            [c.completed_date for c in self.completions],
            reverse=True
        )
        
        if not completion_dates:
            return 0
        
        streak = 0
        
        if self.frequency == 'daily':
            # For daily habits, check consecutive days
            expected_date = today
            
            # Allow for today not being completed yet
            if completion_dates and completion_dates[0] != today:
                expected_date = today - timedelta(days=1)
            
            for comp_date in completion_dates:
                if comp_date == expected_date:
                    streak += 1
                    expected_date -= timedelta(days=1)
                elif comp_date < expected_date:
                    break
                    
        elif self.frequency == 'weekly':
            # For weekly habits, check if completed at least once per week
            current_week = today.isocalendar()[1]
            current_year = today.year
            
            # Group completions by week
            weeks_completed = set()
            for comp_date in completion_dates:
                week_num = comp_date.isocalendar()[1]
                year = comp_date.year
                weeks_completed.add((year, week_num))
            
            # Count consecutive weeks
            expected_week = current_week
            expected_year = current_year
            
            # Allow for current week not being completed yet
            if (expected_year, expected_week) not in weeks_completed:
                expected_week -= 1
                if expected_week < 1:
                    expected_year -= 1
                    expected_week = 52
            
            while (expected_year, expected_week) in weeks_completed:
                streak += 1
                expected_week -= 1
                if expected_week < 1:
                    expected_year -= 1
                    expected_week = 52
        
        return streak


class Completion(db.Model):
    __tablename__ = 'completions'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id', ondelete='CASCADE'), nullable=False)
    completed_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('habit_id', 'completed_date', name='unique_habit_date'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'completed_date': self.completed_date.isoformat(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
