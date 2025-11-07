"""Access API endpoints."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db import db
from app.models import Access, User
from app.schemas import AccessCreate, AccessResponse

blp = Blueprint('access', __name__, url_prefix='/access', description='Access operations')


@blp.route('/')
class AccessList(MethodView):
    """Access list endpoint."""
    
    @blp.response(200, AccessResponse(many=True))
    def get(self):
        """List all access logs."""
        accesses = Access.query.all()
        return accesses
    
    @blp.arguments(AccessCreate)
    @blp.response(201, AccessResponse)
    def post(self, access_data):
        """Create a new access log."""
        # Verify user exists
        user = User.query.get(access_data['user_id'])
        if not user:
            abort(404, message="User not found")
        
        access = Access(**access_data)
        db.session.add(access)
        db.session.commit()
        return access


@blp.route('/<int:access_id>')
class AccessDetail(MethodView):
    """Access detail endpoint."""
    
    @blp.response(200, AccessResponse)
    def get(self, access_id):
        """Get an access log by ID."""
        access = Access.query.get_or_404(access_id)
        return access
    
    @blp.response(204)
    def delete(self, access_id):
        """Delete an access log."""
        access = Access.query.get_or_404(access_id)
        db.session.delete(access)
        db.session.commit()
        return ''
