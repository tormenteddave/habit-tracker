"""
Tests for Completion API endpoints.
"""
import json
from datetime import date


def test_create_completion(client, sample_habit):
    """Test logging a habit completion."""
    today = date.today().isoformat()
    
    response = client.post(
        f'/api/habits/{sample_habit["id"]}/completions',
        data=json.dumps({
            'completed_date': today,
            'notes': 'Completed morning routine'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert response.json['completed_date'] == today
    assert response.json['notes'] == 'Completed morning routine'


def test_create_completion_duplicate(client, sample_habit):
    """Test that duplicate completions for the same date are rejected."""
    today = date.today().isoformat()
    
    # Create first completion
    client.post(
        f'/api/habits/{sample_habit["id"]}/completions',
        data=json.dumps({'completed_date': today}),
        content_type='application/json'
    )
    
    # Try to create duplicate
    response = client.post(
        f'/api/habits/{sample_habit["id"]}/completions',
        data=json.dumps({'completed_date': today}),
        content_type='application/json'
    )
    
    assert response.status_code == 409  # Conflict
    assert 'error' in response.json
