from flask import Blueprint, request, jsonify
from app import db
from app.models import Category

bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@bp.route('', methods=['GET'])
def get_categories():
    """Retrieve all categories."""
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200


@bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    """Retrieve a single category by ID."""
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict()), 200


@bp.route('', methods=['POST'])
def create_category():
    """Create a new category."""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Check for duplicate
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category with this name already exists'}), 409
    
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    """Update an existing category."""
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Check for duplicate (excluding current category)
    existing = Category.query.filter_by(name=data['name']).first()
    if existing and existing.id != id:
        return jsonify({'error': 'Category with this name already exists'}), 409
    
    category.name = data['name']
    db.session.commit()
    
    return jsonify(category.to_dict()), 200


@bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    """Delete a category."""
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted successfully'}), 200
