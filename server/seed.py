# seed.py
from server.app import app, db
from server.models import User, Property, PropertyImage, PropertyAmenity, Booking, Payment, Review
from datetime import datetime

def seed_database():
    """Seed the database with initial data"""
    with app.app_context():
        # Clear existing data
        db.session.query(Review).delete()
        db.session.query(Payment).delete()
        db.session.query(Booking).delete()
        db.session.query(PropertyAmenity).delete()
        db.session.query(PropertyImage).delete()
        db.session.query(Property).delete()
        db.session.query(User).delete()

        # --- Seed Users ---
        users = [
            User(name='Admin User', email='admin@rentease.com', role='admin'),
            User(name='Jeremy Jomo', email='jomo.kamau@gmail.com', role='landlord'),
            User(name='Test Tenant', email='tenant@example.com', role='tenant'),
        ]

        users[0].password = "admin123"
        users[1].password = "landlord123"
        users[2].password = "tenant123"

        db.session.add_all(users)
        db.session.commit()

        # --- Seed Properties ---
        locations = [
            'Westlands, Nairobi', 'Kilimani, Nairobi', 'Karen, Nairobi',
            'Lavington, Nairobi', 'Kileleshwa, Nairobi', 'Runda, Nairobi',
            'South B, Nairobi', 'Upper Hill, Nairobi'
        ]

        properties = [
            Property(
                title='Modern Apartment in Westlands',
                description='Beautiful 2-bedroom apartment with city views',
                rent_price=45000.00,
                location=locations[0],
                image_url='https://images.unsplash.com/photo-1564013799919-ab600027ffc6',
                landlord_id=users[1].id,
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Spacious Karen House',
                description='3-bedroom family house with garden',
                rent_price=85000.00,
                location=locations[2],
                image_url='https://images.unsplash.com/photo-1507089947368-19c1da9775ae',
                landlord_id=users[1].id,
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Kilimani Studio',
                description='Cozy studio apartment near amenities',
                rent_price=25000.00,
                location=locations[1],
                image_url='https://images.unsplash.com/photo-1554995207-c18c203602cb',
                landlord_id=users[2].id,
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Lavington Bungalow',
                description='Classic 2-bedroom bungalow with private garden',
                rent_price=65000.00,
                location=locations[3],
                image_url='https://images.unsplash.com/photo-1449247709967-d4461a6a6103',
                landlord_id=users[2].id,
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Kileleshwa Apartment',
                description='Modern 1-bedroom with balcony and 24/7 security',
                rent_price=35000.00,
                location=locations[4],
                image_url='https://images.unsplash.com/photo-1598928506311-c55ded91a20c',
                landlord_id=users[1].id,
                available=False,
                created_at=datetime.now()
            )
        ]

        for property in properties:
            db.session.add(property)
        db.session.flush()

        # --- Seed Property Images ---
        property_images = [
            PropertyImage(
                property_id=properties[0].id,
                image_url='https://images.unsplash.com/photo-1564013799919-ab600027ffc6',
                caption='Modern living room with city views',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[0].id,
                image_url='https://images.unsplash.com/photo-1586023492125-27b2c045efd7',
                caption='Spacious bedroom with balcony',
                is_primary=False,
                sort_order=2,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[1].id,
                image_url='https://images.unsplash.com/photo-1502672260266-1c1ef2d93688',
                caption='Beautiful Karen garden and outdoor area',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[2].id,
                image_url='https://images.unsplash.com/photo-1554995207-c18c203602cb',
                caption='Modern Kilimani studio kitchenette',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[3].id,
                image_url='https://images.unsplash.com/photo-1505693416388-ac5ce068fe85',
                caption='Cozy bungalow living room',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[4].id,
                image_url='https://images.unsplash.com/photo-1598928506311-c55ded91a20c',
                caption='Contemporary Kileleshwa bedroom',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            )
        ]

        db.session.add_all(property_images)
        db.session.flush()

        # --- Seed Property Amenities ---
        amenities = [
            PropertyAmenity(
                property_id=properties[0].id,
                amenity_name='wifi',
                description='High-speed internet included',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[0].id,
                amenity_name='parking',
                description='1 parking slot available',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[1].id,
                amenity_name='pool',
                description='Private swimming pool and garden',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[2].id,
                amenity_name='gym',
                description='Access to shared gym facility',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[3].id,
                amenity_name='garden',
                description='Spacious outdoor garden area',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[4].id,
                amenity_name='security',
                description='24/7 security and CCTV surveillance',
                included=True
            )
        ]

        db.session.add_all(amenities)
        db.session.flush()

        # --- Seed Bookings ---
        bookings = [
            Booking(
                tenant_id=users[2].id,  # Test Tenant
                property_id=properties[0].id,
                start_date=datetime(2024, 1, 15),
                end_date=datetime(2024, 12, 15),
                status='approved',
                created_at=datetime.now()
            ),
            Booking(
                tenant_id=users[2].id,
                property_id=properties[1].id,
                start_date=datetime(2024, 3, 1),
                end_date=datetime(2024, 9, 1),
                status='pending',
                created_at=datetime.now()
            )
        ]

        db.session.add_all(bookings)
        db.session.flush()

        # --- Seed Payments ---
        payments = [
            Payment(
                booking_id=bookings[0].id,
                tenant_id=users[2].id,
                landlord_id=users[1].id,
                amount=45000.00,
                payment_method='bank_transfer',
                status='completed',
                transaction_id='TXN00123456',
                paid_at=datetime.now(),
                created_at=datetime.now()
            ),
            Payment(
                booking_id=bookings[1].id,
                tenant_id=users[2].id,
                landlord_id=users[1].id,
                amount=85000.00,
                payment_method='credit_card',
                status='pending',
                transaction_id='TXN00123457',
                paid_at=None,
                created_at=datetime.now()
            )
        ]

        db.session.add_all(payments)
        db.session.flush()

        # --- Seed Reviews ---
        reviews = [
            Review(
                booking_id=bookings[0].id,
                tenant_id=users[2].id,
                property_id=properties[0].id,
                landlord_id=users[1].id,
                rating=5,
                review_text='Great apartment! Perfect location and amazing service.',
                landlord_reply='Thank you for your kind feedback!',
                is_approved=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]

        db.session.add_all(reviews)
        db.session.commit()

        print("✅ Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
