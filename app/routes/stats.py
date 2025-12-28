from flask import Blueprint, request, jsonify
from app.models import Habit
from datetime import date, timedelta

bp = Blueprint('stats', __name__, url_prefix='/api/stats')


@bp.route('/summary', methods=['GET'])
def get_summary():
    """Get a summary of all habits with statistics."""
    habits = Habit.query.filter_by(is_active=True).all()
    today = date.today()
    
    # Get current week boundaries
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    summary = []
    for habit in habits:
        # Calculate weekly total
        weekly_total = sum(
            1 for c in habit.completions 
            if week_start <= c.completed_date <= week_end
        )
        
        # Calculate monthly total
        monthly_total = sum(
            1 for c in habit.completions 
            if c.completed_date.year == today.year and c.completed_date.month == today.month
        )
        
        summary.append({
            'id': habit.id,
            'name': habit.name,
            'frequency': habit.frequency,
            'category_name': habit.category.name if habit.category else None,
            'current_streak': habit.calculate_streak(),
            'weekly_total': weekly_total,
            'monthly_total': monthly_total
        })
    
    return jsonify({
        'date': today.isoformat(),
        'habits': summary
    }), 200


@bp.route('/weekly', methods=['GET'])
def get_weekly_stats():
    """Get weekly totals for all habits."""
    today = date.today()
    year = request.args.get('year', today.year, type=int)
    week = request.args.get('week', today.isocalendar()[1], type=int)
    
    # Calculate week boundaries
    jan_first = date(year, 1, 1)
    week_start = jan_first + timedelta(days=(week - 1) * 7 - jan_first.weekday())
    week_end = week_start + timedelta(days=6)
    
    habits = Habit.query.filter_by(is_active=True).all()
    
    results = []
    for habit in habits:
        completions = [
            c for c in habit.completions 
            if week_start <= c.completed_date <= week_end
        ]
        results.append({
            'habit_id': habit.id,
            'habit_name': habit.name,
            'frequency': habit.frequency,
            'total_completions': len(completions),
            'completion_dates': [c.completed_date.isoformat() for c in completions]
        })
    
    return jsonify({
        'year': year,
        'week': week,
        'week_start': week_start.isoformat(),
        'week_end': week_end.isoformat(),
        'habits': results
    }), 200


@bp.route('/monthly', methods=['GET'])
def get_monthly_stats():
    """Get monthly totals for all habits."""
    today = date.today()
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)
    
    habits = Habit.query.filter_by(is_active=True).all()
    
    results = []
    for habit in habits:
        completions = [
            c for c in habit.completions 
            if c.completed_date.year == year and c.completed_date.month == month
        ]
        results.append({
            'habit_id': habit.id,
            'habit_name': habit.name,
            'frequency': habit.frequency,
            'total_completions': len(completions),
            'completion_dates': [c.completed_date.isoformat() for c in completions]
        })
    
    return jsonify({
        'year': year,
        'month': month,
        'habits': results
    }), 200
