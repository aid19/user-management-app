from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create tables
with app.app_context():
    db.create_all()

# Validation Functions
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def email_exists(email, exclude_id=None):
    query = User.query.filter_by(email=email)
    if exclude_id:
        query = query.filter(User.id != exclude_id)
    return query.first() is not None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')
    
    if sort_by == 'email':
        if sort_order == 'desc':
            users = User.query.order_by(User.email.desc()).all()
        else:
            users = User.query.order_by(User.email.asc()).all()
    else:
        if sort_order == 'desc':
            users = User.query.order_by(User.name.desc()).all()
        else:
            users = User.query.order_by(User.name.asc()).all()
    
    return jsonify([user.to_dict() for user in users])

@app.route('/api/search', methods=['GET'])
def search_users():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])
    
    users = User.query.filter(User.name.ilike(f'%{query}%')).all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if email_exists(email):
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if email != user.email and email_exists(email, user_id):
        return jsonify({'error': 'Email already exists'}), 400
    
    user.name = name
    user.email = email
    db.session.commit()
    
    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
