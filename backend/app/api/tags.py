"""Tag check API endpoint."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models import User
from app.schemas import UserResponse

blp = Blueprint('tags', __name__, url_prefix='/tags', description='Tag verification operations')


@blp.route('/<string:tag>/check')
class TagCheck(MethodView):
    """Tag check endpoint."""
    
    @blp.response(200, UserResponse)
    def get(self, tag):
        """Check if an RFID tag is registered and return the associated user."""
        user = User.query.filter_by(rfid_tag=tag).first()
        if not user:
            abort(404, message="Tag not found")
        return user
