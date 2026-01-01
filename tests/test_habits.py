"""
Tests for Habit API endpoints.
"""
import json


def test_get_habits_empty(client):
    """Test getting habits when none exist."""
    response = client.get('/api/habits')
    
    assert response.status_code == 200
    assert response.json == []


def test_create_habit(client, sample_category):
    """Test creating a new habit."""
    response = client.post(
        '/api/habits',
        data=json.dumps({
            'name': 'Meditation',
            'description': '10 minutes of meditation',
            'frequency': 'daily',
            'category_id': sample_category['id']
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert response.json['name'] == 'Meditation'
    assert response.json['frequency'] == 'daily'


def test_create_habit_invalid_frequency(client):
    """Test creating a habit with invalid frequency."""
    response = client.post(
        '/api/habits',
        data=json.dumps({
            'name': 'Test Habit',
            'frequency': 'monthly'  # Invalid - only 'daily' or 'weekly' allowed
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'error' in response.json
