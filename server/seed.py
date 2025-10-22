import os
import sys
from datetime import datetime, timedelta
import random
from faker import Faker

# Add the parent directory to the path to import your models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.property import Property
from app.models.booking import Booking

fake = Faker()

def seed_database():
    """Seed the database with sample data"""
    app = create_app()
    
    with app.app_context():
        print("🗑️  Clearing existing data...")
        # Clear existing data (in correct order due to foreign key constraints)
        Booking.query.delete()
        Property.query.delete()
        User.query.delete()
        db.session.commit()
        
        print("👥 Creating users...")
        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@rentease.com",
            password="$2b$12$Qq9l7C7rC7C7C7C7C7C7C.C7C7C7C7C7C7C7C7C7C7C7C7C7C7C",  # "password"
            role="admin",
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        
        # Create landlords
        landlords = []
        for i in range(3):
            landlord = User(
                name=fake.name(),
                email=f"landlord{i+1}@example.com",
                password="$2b$12$Qq9l7C7rC7C7C7C7C7C7C.C7C7C7C7C7C7C7C7C7C7C7C7C7C7C",  # "password"
                role="landlord",
                created_at=fake.date_time_this_year()
            )
            landlords.append(landlord)
            db.session.add(landlord)
        
        # Create tenants
        tenants = []
        for i in range(10):
            tenant = User(
                name=fake.name(),
                email=f"tenant{i+1}@example.com",
                password="$2b$12$Qq9l7C7rC7C7C7C7C7C.C7C7C7C7C7C7C7C7C7C7C7C7C7C7C",  # "password"
                role="tenant",
                created_at=fake.date_time_this_year()
            )
            tenants.append(tenant)
            db.session.add(tenant)
        
        db.session.commit()
        print(f"✅ Created {len(landlords) + len(tenants) + 1} users")
        
        print("🏠 Creating properties...")
        # Sample property data
        property_data = [
            {
                "title": "Modern Downtown Apartment",
                "description": "Beautiful modern apartment in the heart of downtown with great amenities and stunning city views.",
                "rent_price": 1200.00,
                "location": "Nairobi CBD"
            },
            {
                "title": "Cozy Suburban House",
                "description": "Spacious 3-bedroom house in a quiet suburban neighborhood. Perfect for families.",
                "rent_price": 800.00,
                "location": "Westlands"
            },
            {
                "title": "Luxury Villa with Pool",
                "description": "Stunning luxury villa featuring a private pool, garden, and modern furnishings.",
                "rent_price": 2500.00,
                "location": "Karen"
            },
            {
                "title": "Studio Apartment near University",
                "description": "Compact and affordable studio apartment, ideal for students. Close to campus and public transport.",
                "rent_price": 450.00,
                "location": "Kilimani"
            },
            {
                "title": "Executive Penthouse",
                "description": "Luxurious penthouse with panoramic views, high-end finishes, and premium amenities.",
                "rent_price": 1800.00,
                "location": "Upper Hill"
            },
            {
                "title": "Garden Cottage",
                "description": "Charming cottage with a beautiful garden, perfect for couples or small families.",
                "rent_price": 600.00,
                "location": "Lavington"
            },
            {
                "title": "Modern Loft",
                "description": "Industrial-style loft with high ceilings, exposed brick, and modern appliances.",
                "rent_price": 950.00,
                "location": "South B"
            },
            {
                "title": "Beachfront Apartment",
                "description": "Beautiful apartment with direct beach access and ocean views. Fully furnished.",
                "rent_price": 1100.00,
                "location": "Mombasa"
            }
        ]
        
        properties = []
        image_urls = [
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=500",
            "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=500",
            "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=500",
            "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?w=500"
        ]
        
        for i, prop_data in enumerate(property_data):
            property = Property(
                title=prop_data["title"],
                description=prop_data["description"],
                rent_price=prop_data["rent_price"],
                location=prop_data["location"],
                image_url=image_urls[i % len(image_urls)],
                landlord_id=landlords[i % len(landlords)].id,
                available=random.choice([True, True, True, False]),  # 75% available
                created_at=fake.date_time_this_year()
            )
            properties.append(property)
            db.session.add(property)
        
        db.session.commit()
        print(f"✅ Created {len(properties)} properties")
        
        print("📅 Creating bookings...")
        bookings = []
        status_options = ["pending", "approved", "cancelled"]
        
        # Create bookings for various properties and tenants
        for _ in range(15):
            tenant = random.choice(tenants)
            property = random.choice(properties)
            
            # Generate random dates
            start_date = fake.date_between(start_date='today', end_date='+30 days')
            end_date = start_date + timedelta(days=random.randint(3, 14))
            
            booking = Booking(
                tenant_id=tenant.id,
                property_id=property.id,
                start_date=start_date,
                end_date=end_date,
                status=random.choice(status_options),
                created_at=fake.date_time_this_year()
            )
            bookings.append(booking)
            db.session.add(booking)
        
        db.session.commit()
        print(f"✅ Created {len(bookings)} bookings")
        
        print("🎉 Database seeding completed successfully!")
        print("\n📊 Sample Data Summary:")
        print(f"   👥 Users: {User.query.count()} total")
        print(f"      - Admins: {User.query.filter_by(role='admin').count()}")
        print(f"      - Landlords: {User.query.filter_by(role='landlord').count()}")
        print(f"      - Tenants: {User.query.filter_by(role='tenant').count()}")
        print(f"   🏠 Properties: {Property.query.count()} total")
        print(f"      - Available: {Property.query.filter_by(available=True).count()}")
        print(f"      - Occupied: {Property.query.filter_by(available=False).count()}")
        print(f"   📅 Bookings: {Booking.query.count()} total")
        print(f"      - Pending: {Booking.query.filter_by(status='pending').count()}")
        print(f"      - Approved: {Booking.query.filter_by(status='approved').count()}")
        print(f"      - Cancelled: {Booking.query.filter_by(status='cancelled').count()}")
        
        print("\n🔑 Test Login Credentials:")
        print("   Admin:     admin@rentease.com / password")
        print("   Landlord1: landlord1@example.com / password")
        print("   Tenant1:   tenant1@example.com / password")

if __name__ == "__main__":
    seed_database()