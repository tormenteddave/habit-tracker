"""
Tests for Category API endpoints.
"""
import json


def test_get_categories_empty(client):
    """Test getting categories when none exist."""
    response = client.get('/api/categories')
    
    assert response.status_code == 200
    assert response.json == []


def test_create_category(client):
    """Test creating a new category."""
    response = client.post(
        '/api/categories',
        data=json.dumps({'name': 'Productivity'}),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert response.json['name'] == 'Productivity'
    assert 'id' in response.json


def test_delete_category(client, sample_category):
    """Test deleting a category."""
    response = client.delete(f'/api/categories/{sample_category["id"]}')
    
    assert response.status_code == 200
    
    # Verify it's actually deleted
    get_response = client.get(f'/api/categories/{sample_category["id"]}')
    assert get_response.status_code == 404
