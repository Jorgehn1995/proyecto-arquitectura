"""API endpoints for thresholds."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db import db
from app.models import Threshold
from app.schemas import (
    ThresholdCreateSchema,
    ThresholdUpdateSchema,
    ThresholdResponseSchema,
    SensorReadingSchema
)

blp = Blueprint(
    'thresholds',
    __name__,
    url_prefix='/thresholds',
    description='Operations on thresholds'
)


@blp.route('')
class ThresholdList(MethodView):
    """Threshold list endpoint."""
    
    @blp.response(200, ThresholdResponseSchema)
    def get(self):
        """Get the current threshold (single record)."""
        threshold = Threshold.query.first()
        if not threshold:
            abort(404, message="No threshold configured")
        return threshold
    
    @blp.arguments(ThresholdCreateSchema)
    @blp.response(201, ThresholdResponseSchema)
    def post(self, data):
        """Create or update the threshold (only one record allowed)."""
        # Check if threshold already exists
        threshold = Threshold.query.first()
        
        # Validate ranges
        if data['min_humidity'] > data['max_humidity']:
            abort(400, message="min_humidity must be less than or equal to max_humidity")
        if data['min_temperature'] > data['max_temperature']:
            abort(400, message="min_temperature must be less than or equal to max_temperature")
        
        if threshold:
            # Update existing threshold
            threshold.min_humidity = data['min_humidity']
            threshold.max_humidity = data['max_humidity']
            threshold.min_temperature = data['min_temperature']
            threshold.max_temperature = data['max_temperature']
        else:
            # Create new threshold
            threshold = Threshold(**data)
            db.session.add(threshold)
        
        db.session.commit()
        return threshold


@blp.route('/<int:id>')
class ThresholdById(MethodView):
    """Threshold by ID endpoint."""
    
    @blp.response(200, ThresholdResponseSchema)
    def get(self, id):
        """Get threshold by ID."""
        threshold = Threshold.query.get_or_404(id, description="Threshold not found")
        return threshold
    
    @blp.arguments(ThresholdUpdateSchema)
    @blp.response(200, ThresholdResponseSchema)
    def put(self, data, id):
        """Update threshold."""
        threshold = Threshold.query.get_or_404(id, description="Threshold not found")
        
        # Validate ranges if both min and max are provided
        if 'min_humidity' in data and 'max_humidity' in data:
            if data['min_humidity'] > data['max_humidity']:
                abort(400, message="min_humidity must be less than or equal to max_humidity")
        elif 'min_humidity' in data:
            if data['min_humidity'] > threshold.max_humidity:
                abort(400, message="min_humidity must be less than or equal to max_humidity")
        elif 'max_humidity' in data:
            if threshold.min_humidity > data['max_humidity']:
                abort(400, message="min_humidity must be less than or equal to max_humidity")
        
        if 'min_temperature' in data and 'max_temperature' in data:
            if data['min_temperature'] > data['max_temperature']:
                abort(400, message="min_temperature must be less than or equal to max_temperature")
        elif 'min_temperature' in data:
            if data['min_temperature'] > threshold.max_temperature:
                abort(400, message="min_temperature must be less than or equal to max_temperature")
        elif 'max_temperature' in data:
            if threshold.min_temperature > data['max_temperature']:
                abort(400, message="min_temperature must be less than or equal to max_temperature")
        
        for key, value in data.items():
            setattr(threshold, key, value)
        
        db.session.commit()
        return threshold
    
    @blp.response(204)
    def delete(self, id):
        """Delete threshold."""
        threshold = Threshold.query.get_or_404(id, description="Threshold not found")
        db.session.delete(threshold)
        db.session.commit()
        return ''


@blp.route('/validate')
class ThresholdValidate(MethodView):
    """Validate sensor readings against thresholds."""
    
    @blp.arguments(SensorReadingSchema)
    @blp.response(200, description="Reading is within thresholds")
    @blp.alt_response(400, description="Reading is outside thresholds")
    def post(self, data):
        """Validate humidity and temperature against configured thresholds.
        
        Returns 200 if within thresholds, 400 if outside thresholds.
        """
        threshold = Threshold.query.first()
        if not threshold:
            abort(404, message="No threshold configured")
        
        humidity = data['humidity']
        temperature = data['temperature']
        
        errors = []
        
        # Validate humidity
        if humidity < threshold.min_humidity:
            errors.append(f"Humidity {humidity} is below minimum threshold {threshold.min_humidity}")
        elif humidity > threshold.max_humidity:
            errors.append(f"Humidity {humidity} is above maximum threshold {threshold.max_humidity}")
        
        # Validate temperature
        if temperature < threshold.min_temperature:
            errors.append(f"Temperature {temperature} is below minimum threshold {threshold.min_temperature}")
        elif temperature > threshold.max_temperature:
            errors.append(f"Temperature {temperature} is above maximum threshold {threshold.max_temperature}")
        
        if errors:
            return {
                "status": "outside_thresholds",
                "message": "Sensor readings are outside configured thresholds",
                "errors": errors,
                "humidity": humidity,
                "temperature": temperature,
                "thresholds": {
                    "min_humidity": threshold.min_humidity,
                    "max_humidity": threshold.max_humidity,
                    "min_temperature": threshold.min_temperature,
                    "max_temperature": threshold.max_temperature
                }
            }, 400
        
        return {
            "status": "ok",
            "message": "Sensor readings are within thresholds",
            "humidity": humidity,
            "temperature": temperature,
            "thresholds": {
                "min_humidity": threshold.min_humidity,
                "max_humidity": threshold.max_humidity,
                "min_temperature": threshold.min_temperature,
                "max_temperature": threshold.max_temperature
            }
        }, 200
