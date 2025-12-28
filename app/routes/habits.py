from flask import Blueprint, request, jsonify
from app import db
from app.models import Habit
from datetime import date, timedelta

bp = Blueprint('habits', __name__, url_prefix='/api/habits')


@bp.route('', methods=['GET'])
def get_habits():
    """Retrieve all habits with optional filters."""
    query = Habit.query
    
    # Filter by category
    category_id = request.args.get('category_id', type=int)
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Filter by active status
    is_active = request.args.get('is_active')
    if is_active is not None:
        is_active_bool = is_active.lower() == 'true'
        query = query.filter_by(is_active=is_active_bool)
    
    # Filter by frequency
    frequency = request.args.get('frequency')
    if frequency in ['daily', 'weekly']:
        query = query.filter_by(frequency=frequency)
    
    habits = query.all()
    return jsonify([h.to_dict(include_streak=True) for h in habits]), 200


@bp.route('/<int:id>', methods=['GET'])
def get_habit(id):
    """Retrieve a single habit by ID."""
    habit = Habit.query.get_or_404(id)
    return jsonify(habit.to_dict(include_streak=True)), 200


@bp.route('', methods=['POST'])
def create_habit():
    """Create a new habit."""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    if 'frequency' not in data or data['frequency'] not in ['daily', 'weekly']:
        return jsonify({'error': 'Frequency must be "daily" or "weekly"'}), 400
    
    habit = Habit(
        name=data['name'],
        description=data.get('description'),
        frequency=data['frequency'],
        category_id=data.get('category_id')
    )
    db.session.add(habit)
    db.session.commit()
    
    return jsonify(habit.to_dict(include_streak=True)), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_habit(id):
    """Update an existing habit."""
    habit = Habit.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'name' in data:
        habit.name = data['name']
    if 'description' in data:
        habit.description = data['description']
    if 'frequency' in data:
        if data['frequency'] not in ['daily', 'weekly']:
            return jsonify({'error': 'Frequency must be "daily" or "weekly"'}), 400
        habit.frequency = data['frequency']
    if 'category_id' in data:
        habit.category_id = data['category_id']
    if 'is_active' in data:
        habit.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify(habit.to_dict(include_streak=True)), 200


@bp.route('/<int:id>', methods=['DELETE'])
def delete_habit(id):
    """Permanently delete a habit and all its completions."""
    habit = Habit.query.get_or_404(id)
    db.session.delete(habit)
    db.session.commit()
    
    return jsonify({'message': 'Habit deleted successfully'}), 200


@bp.route('/<int:id>/streak', methods=['GET'])
def get_streak(id):
    """Get the current streak for a specific habit."""
    habit = Habit.query.get_or_404(id)
    streak = habit.calculate_streak()
    
    return jsonify({
        'habit_id': id,
        'habit_name': habit.name,
        'current_streak': streak,
        'frequency': habit.frequency
    }), 200


@bp.route('/<int:id>/stats', methods=['GET'])
def get_habit_stats(id):
    """Get statistics for a habit."""
    habit = Habit.query.get_or_404(id)
    
    today = date.today()
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)
    week = request.args.get('week', today.isocalendar()[1], type=int)
    
    # Calculate weekly total
    # Get the start and end of the specified week
    jan_first = date(year, 1, 1)
    week_start = jan_first + timedelta(days=(week - 1) * 7 - jan_first.weekday())
    week_end = week_start + timedelta(days=6)
    
    weekly_total = sum(
        1 for c in habit.completions 
        if week_start <= c.completed_date <= week_end
    )
    
    # Calculate monthly total
    monthly_total = sum(
        1 for c in habit.completions 
        if c.completed_date.year == year and c.completed_date.month == month
    )
    
    return jsonify({
        'habit_id': id,
        'habit_name': habit.name,
        'current_streak': habit.calculate_streak(),
        'weekly_total': weekly_total,
        'monthly_total': monthly_total,
        'week': week,
        'month': month,
        'year': year
    }), 200
