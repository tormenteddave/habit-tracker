from flask import Blueprint, request, jsonify
from app import db
from app.models import Habit, Completion
from datetime import datetime

bp = Blueprint('completions', __name__)


@bp.route('/api/habits/<int:habit_id>/completions', methods=['GET'])
def get_completions(habit_id):
    """Get all completions for a habit."""
    habit = Habit.query.get_or_404(habit_id)
    
    query = Completion.query.filter_by(habit_id=habit_id)
    
    # Filter by date range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Completion.completed_date >= start)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Completion.completed_date <= end)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400
    
    completions = query.order_by(Completion.completed_date.desc()).all()
    
    return jsonify({
        'habit_id': habit_id,
        'habit_name': habit.name,
        'completions': [c.to_dict() for c in completions]
    }), 200


@bp.route('/api/habits/<int:habit_id>/completions', methods=['POST'])
def create_completion(habit_id):
    """Log a completion for a habit."""
    habit = Habit.query.get_or_404(habit_id)
    data = request.get_json()
    
    if not data or 'completed_date' not in data:
        return jsonify({'error': 'completed_date is required'}), 400
    
    try:
        completed_date = datetime.strptime(data['completed_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Check for duplicate completion
    existing = Completion.query.filter_by(
        habit_id=habit_id, 
        completed_date=completed_date
    ).first()
    
    if existing:
        return jsonify({'error': 'Completion already exists for this date'}), 409
    
    completion = Completion(
        habit_id=habit_id,
        completed_date=completed_date,
        notes=data.get('notes')
    )
    db.session.add(completion)
    db.session.commit()
    
    return jsonify(completion.to_dict()), 201


@bp.route('/api/completions/<int:id>', methods=['DELETE'])
def delete_completion(id):
    """Delete a specific completion entry."""
    completion = Completion.query.get_or_404(id)
    db.session.delete(completion)
    db.session.commit()
    
    return jsonify({'message': 'Completion deleted successfully'}), 200
