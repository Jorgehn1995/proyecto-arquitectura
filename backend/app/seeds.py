"""Database seeding script."""
from datetime import datetime
from app.db import db
from app.models import User, Read, Pump, Sensor, Fan, Smoke, Access, Threshold


def seed_database():
    """Populate database with initial test data."""
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    print("🌱 Seeding database...")
    
    # Create users
    jorge = User(
        first_name="Jorge",
        last_name="Hernández",
        email="jorge@example.com",
        rfid_tag="ABC123"
    )
    
    ana = User(
        first_name="Ana",
        last_name="Pérez",
        email="ana@example.com",
        rfid_tag=None
    )
    
    luis = User(
        first_name="Luis",
        last_name="Martínez",
        email="luis@example.com",
        rfid_tag="XYZ789"
    )
    
    db.session.add_all([jorge, ana, luis])
    db.session.flush()
    
    # Create reads with related entities
    read1 = Read(
        name="Read 1",
        user_id=jorge.id,
        timestamp=datetime.utcnow()
    )
    db.session.add(read1)
    db.session.flush()
    
    pump1 = Pump(
        read_id=read1.id,
        status=True
    )
    
    sensor1 = Sensor(
        read_id=read1.id,
        humidity=45.5,
        temperature=24.1
    )
    
    fan1 = Fan(
        read_id=read1.id,
        status=False
    )
    
    smoke1 = Smoke(
        read_id=read1.id,
        status=False
    )
    
    db.session.add_all([pump1, sensor1, fan1, smoke1])
    
    # Create second read
    read2 = Read(
        name="Read 2",
        user_id=ana.id,
        timestamp=datetime.utcnow()
    )
    db.session.add(read2)
    db.session.flush()
    
    pump2 = Pump(
        read_id=read2.id,
        status=False
    )
    
    sensor2 = Sensor(
        read_id=read2.id,
        humidity=60.2,
        temperature=22.5
    )
    
    fan2 = Fan(
        read_id=read2.id,
        status=True
    )
    
    smoke2 = Smoke(
        read_id=read2.id,
        status=False
    )
    
    db.session.add_all([pump2, sensor2, fan2, smoke2])
    
    # Create access logs
    access1 = Access(user_id=jorge.id, timestamp=datetime.utcnow())
    access2 = Access(user_id=luis.id, timestamp=datetime.utcnow())
    
    db.session.add_all([access1, access2])
    
    # Create default threshold
    threshold = Threshold(
        min_humidity=30.0,
        max_humidity=70.0,
        min_temperature=18.0,
        max_temperature=28.0
    )
    db.session.add(threshold)
    
    # Commit all changes
    db.session.commit()
    
    print(f"✅ Created {User.query.count()} users")
    print(f"✅ Created {Read.query.count()} reads")
    print(f"✅ Created {Pump.query.count()} pumps")
    print(f"✅ Created {Sensor.query.count()} sensors")
    print(f"✅ Created {Fan.query.count()} fans")
    print(f"✅ Created {Smoke.query.count()} smokes")
    print(f"✅ Created {Access.query.count()} access logs")
    print(f"✅ Created threshold (humidity: 30-70%, temperature: 18-28°C)")
