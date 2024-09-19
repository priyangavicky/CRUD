from flask import Flask, request, jsonify
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'], active=data['active'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Get a user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'active': user.active
    })

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'active': user.active
        }
        all_users.append(user_data)
    return jsonify(all_users), 200


# Update a user by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.username = data['username']
    user.password = data['password']
    user.active = data['active']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# Delete a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
