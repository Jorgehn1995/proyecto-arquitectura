"""User API endpoints."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db import db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse

blp = Blueprint('users', __name__, url_prefix='/users', description='User operations')


@blp.route('/')
class UserList(MethodView):
    """User list endpoint."""
    
    @blp.response(200, UserResponse(many=True))
    def get(self):
        """List all users."""
        users = User.query.all()
        return users
    
    @blp.arguments(UserCreate)
    @blp.response(201, UserResponse)
    def post(self, user_data):
        """Create a new user."""
        # Check if email already exists
        if User.query.filter_by(email=user_data['email']).first():
            abort(400, message="Email already exists")
        
        # Check if rfid_tag already exists (if provided)
        if user_data.get('rfid_tag'):
            if User.query.filter_by(rfid_tag=user_data['rfid_tag']).first():
                abort(400, message="RFID tag already exists")
        
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route('/<int:user_id>')
class UserDetail(MethodView):
    """User detail endpoint."""
    
    @blp.response(200, UserResponse)
    def get(self, user_id):
        """Get a user by ID."""
        user = User.query.get_or_404(user_id)
        return user
    
    @blp.arguments(UserUpdate)
    @blp.response(200, UserResponse)
    def put(self, user_data, user_id):
        """Update a user."""
        user = User.query.get_or_404(user_id)
        
        # Check email uniqueness
        if 'email' in user_data and user_data['email'] != user.email:
            if User.query.filter_by(email=user_data['email']).first():
                abort(400, message="Email already exists")
        
        # Check rfid_tag uniqueness
        if 'rfid_tag' in user_data and user_data['rfid_tag'] != user.rfid_tag:
            if user_data['rfid_tag'] and User.query.filter_by(rfid_tag=user_data['rfid_tag']).first():
                abort(400, message="RFID tag already exists")
        
        for key, value in user_data.items():
            setattr(user, key, value)
        
        db.session.commit()
        return user
    
    @blp.response(204)
    def delete(self, user_id):
        """Delete a user."""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return ''
