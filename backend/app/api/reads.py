"""Read API endpoints."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db import db
from app.models import Read, Pump, Sensor, Fan, Smoke
from app.schemas import ReadCreate, ReadUpdate, ReadResponse

blp = Blueprint('reads', __name__, url_prefix='/reads', description='Read operations')


@blp.route('/')
class ReadList(MethodView):
    """Read list endpoint."""
    
    @blp.response(200, ReadResponse(many=True))
    def get(self):
        """List all reads."""
        reads = Read.query.all()
        return reads
    
    @blp.arguments(ReadCreate)
    @blp.response(201, ReadResponse)
    def post(self, read_data):
        """Create a new read with optional pump, sensor, fan, and smoke."""
        # Extract nested data
        pump_data = read_data.pop('pump', None)
        sensor_data = read_data.pop('sensor', None)
        fan_data = read_data.pop('fan', None)
        smoke_data = read_data.pop('smoke', None)
        
        # Create read
        read = Read(**read_data)
        db.session.add(read)
        db.session.flush()  # Get read.id before creating related entities
        
        # Create related entities
        if pump_data:
            pump = Pump(read_id=read.id, **pump_data)
            db.session.add(pump)
        
        if sensor_data:
            sensor = Sensor(read_id=read.id, **sensor_data)
            db.session.add(sensor)
        
        if fan_data:
            fan = Fan(read_id=read.id, **fan_data)
            db.session.add(fan)
        
        if smoke_data:
            smoke = Smoke(read_id=read.id, **smoke_data)
            db.session.add(smoke)
        
        db.session.commit()
        return read


@blp.route('/<int:read_id>')
class ReadDetail(MethodView):
    """Read detail endpoint."""
    
    @blp.response(200, ReadResponse)
    def get(self, read_id):
        """Get a read by ID."""
        read = Read.query.get_or_404(read_id)
        return read
    
    @blp.arguments(ReadUpdate)
    @blp.response(200, ReadResponse)
    def put(self, read_data, read_id):
        """Update a read."""
        read = Read.query.get_or_404(read_id)
        
        for key, value in read_data.items():
            setattr(read, key, value)
        
        db.session.commit()
        return read
    
    @blp.response(204)
    def delete(self, read_id):
        """Delete a read."""
        read = Read.query.get_or_404(read_id)
        db.session.delete(read)
        db.session.commit()
        return ''
