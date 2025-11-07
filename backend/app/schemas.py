"""Marshmallow schemas for request/response validation."""
from marshmallow import Schema, fields, validate


# User schemas
class UserCreateSchema(Schema):
    """Schema for creating a user."""
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    rfid_tag = fields.Str(validate=validate.Length(max=100), allow_none=True)


class UserUpdateSchema(Schema):
    """Schema for updating a user."""
    first_name = fields.Str(validate=validate.Length(min=1, max=100))
    last_name = fields.Str(validate=validate.Length(min=1, max=100))
    email = fields.Email()
    rfid_tag = fields.Str(validate=validate.Length(max=100), allow_none=True)


class UserResponseSchema(Schema):
    """Schema for user response."""
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    rfid_tag = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


# Pump schemas
class PumpCreateSchema(Schema):
    """Schema for creating a pump."""
    status = fields.Bool(required=True)


class PumpResponseSchema(Schema):
    """Schema for pump response."""
    id = fields.Int(dump_only=True)
    status = fields.Bool()
    read_id = fields.Int()


# Sensor schemas
class SensorCreateSchema(Schema):
    """Schema for creating a sensor."""
    humidity = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    temperature = fields.Float(required=True)


class SensorResponseSchema(Schema):
    """Schema for sensor response."""
    id = fields.Int(dump_only=True)
    humidity = fields.Float()
    temperature = fields.Float()
    read_id = fields.Int()


# Fan schemas
class FanCreateSchema(Schema):
    """Schema for creating a fan."""
    status = fields.Bool(required=True)


class FanResponseSchema(Schema):
    """Schema for fan response."""
    id = fields.Int(dump_only=True)
    status = fields.Bool()
    read_id = fields.Int()


# Smoke schemas
class SmokeCreateSchema(Schema):
    """Schema for creating a smoke detector."""
    status = fields.Bool(required=True)


class SmokeResponseSchema(Schema):
    """Schema for smoke detector response."""
    id = fields.Int(dump_only=True)
    status = fields.Bool()
    read_id = fields.Int()


# Read schemas
class ReadCreateSchema(Schema):
    """Schema for creating a read with nested entities."""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    user_id = fields.Int(allow_none=True)
    pump = fields.Nested('PumpCreateSchema', allow_none=True)
    sensor = fields.Nested('SensorCreateSchema', allow_none=True)
    fan = fields.Nested('FanCreateSchema', allow_none=True)
    smoke = fields.Nested('SmokeCreateSchema', allow_none=True)


class ReadUpdateSchema(Schema):
    """Schema for updating a read."""
    name = fields.Str(validate=validate.Length(min=1, max=200))
    user_id = fields.Int(allow_none=True)


class ReadResponseSchema(Schema):
    """Schema for read response."""
    id = fields.Int(dump_only=True)
    name = fields.Str()
    user_id = fields.Int(allow_none=True)
    timestamp = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    pump = fields.Nested('PumpResponseSchema', allow_none=True)
    sensor = fields.Nested('SensorResponseSchema', allow_none=True)
    fan = fields.Nested('FanResponseSchema', allow_none=True)
    smoke = fields.Nested('SmokeResponseSchema', allow_none=True)


# Access schemas
class AccessCreateSchema(Schema):
    """Schema for creating an access log."""
    user_id = fields.Int(required=True)


class AccessResponseSchema(Schema):
    """Schema for access response."""
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    timestamp = fields.DateTime(dump_only=True)


# Threshold schemas
class ThresholdCreateSchema(Schema):
    """Schema for creating a threshold."""
    min_humidity = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    max_humidity = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    min_temperature = fields.Float(required=True)
    max_temperature = fields.Float(required=True)


class ThresholdUpdateSchema(Schema):
    """Schema for updating a threshold."""
    min_humidity = fields.Float(validate=validate.Range(min=0, max=100))
    max_humidity = fields.Float(validate=validate.Range(min=0, max=100))
    min_temperature = fields.Float()
    max_temperature = fields.Float()


class ThresholdResponseSchema(Schema):
    """Schema for threshold response."""
    id = fields.Int(dump_only=True)
    min_humidity = fields.Float()
    max_humidity = fields.Float()
    min_temperature = fields.Float()
    max_temperature = fields.Float()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Schema for validating sensor readings
class SensorReadingSchema(Schema):
    """Schema for validating sensor readings against thresholds."""
    humidity = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    temperature = fields.Float(required=True)


# Keep old names for backward compatibility
UserCreate = UserCreateSchema
UserUpdate = UserUpdateSchema
UserResponse = UserResponseSchema
PumpCreate = PumpCreateSchema
PumpResponse = PumpResponseSchema
SensorCreate = SensorCreateSchema
SensorResponse = SensorResponseSchema
FanCreate = FanCreateSchema
FanResponse = FanResponseSchema
SmokeCreate = SmokeCreateSchema
SmokeResponse = SmokeResponseSchema
ReadCreate = ReadCreateSchema
ReadUpdate = ReadUpdateSchema
ReadResponse = ReadResponseSchema
AccessCreate = AccessCreateSchema
AccessResponse = AccessResponseSchema
ThresholdCreate = ThresholdCreateSchema
ThresholdUpdate = ThresholdUpdateSchema
ThresholdResponse = ThresholdResponseSchema
SensorReading = SensorReadingSchema

