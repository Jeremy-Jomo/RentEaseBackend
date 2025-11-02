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

        #Seed Users
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
            'South B, Nairobi', 'Upper Hill, Nairobi', 'Parklands, Nairobi',
            'Ngong Road, Nairobi', 'Langata, Nairobi', 'Thika Road, Nairobi',
            'Donholm, Nairobi', 'Mombasa Road, Nairobi'
        ]

        properties = [
            Property(title='Modern Apartment in Westlands',
                     description='Beautiful 2-bedroom apartment with city views',
                     rent_price=45000.00,
                     location=locations[0],
                     image_url='https://images.unsplash.com/photo-1564013799919-ab600027ffc6',
                     landlord_id=users[1].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Spacious Karen House',
                     description='3-bedroom family house with garden',
                     rent_price=85000.00,
                     location=locations[2],
                     image_url='https://images.unsplash.com/photo-1507089947368-19c1da9775ae',
                     landlord_id=users[1].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Kilimani Studio',
                     description='Cozy studio apartment near amenities',
                     rent_price=25000.00,
                     location=locations[1],
                     image_url='https://images.unsplash.com/photo-1554995207-c18c203602cb',
                     landlord_id=users[2].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Lavington Bungalow',
                     description='Classic 2-bedroom bungalow with private garden',
                     rent_price=65000.00,
                     location=locations[3],
                     image_url='https://images.unsplash.com/photo-1449247709967-d4461a6a6103',
                     landlord_id=users[2].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Kileleshwa Apartment',
                     description='Modern 1-bedroom with balcony and 24/7 security',
                     rent_price=35000.00,
                     location=locations[4],
                     image_url='https://images.unsplash.com/photo-1598928506311-c55ded91a20c',
                     landlord_id=users[1].id,
                     available=False,
                     created_at=datetime.now()),

            Property(title='Luxury Villa in Runda',
                     description='5-bedroom villa with pool, gym, and large garden',
                     rent_price=180000.00,
                     location=locations[5],
                     image_url='https://images.unsplash.com/photo-1613977257363-707ba9348227',
                     landlord_id=users[1].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='South B Apartment',
                     description='Affordable 2-bedroom apartment near CBD',
                     rent_price=30000.00,
                     location=locations[6],
                     image_url='https://images.unsplash.com/photo-1580587771525-78b9dba3b914',
                     landlord_id=users[1].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Upper Hill Executive Suite',
                     description='1-bedroom furnished apartment ideal for professionals',
                     rent_price=95000.00,
                     location=locations[7],
                     image_url='https://images.unsplash.com/photo-1615874959474-d609969a20ed',
                     landlord_id=users[1].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Parklands Family Apartment',
                     description='3-bedroom apartment with modern kitchen and balcony',
                     rent_price=60000.00,
                     location=locations[8],
                     image_url='https://images.unsplash.com/photo-1505691938895-1758d7feb511',
                     landlord_id=users[2].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Ngong Road Loft',
                     description='Stylish open-plan loft apartment with Wi-Fi',
                     rent_price=55000.00,
                     location=locations[9],
                     image_url='https://images.unsplash.com/photo-1522708323590-d24dbb6b0267',
                     landlord_id=users[2].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Langata Townhouse',
                     description='Spacious 4-bedroom townhouse near Wilson Airport',
                     rent_price=70000.00,
                     location=locations[10],
                     image_url='https://images.unsplash.com/photo-1493809842364-78817add7ffb',
                     landlord_id=users[1].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Thika Road Bedsitter',
                     description='Compact and affordable bedsitter ideal for students',
                     rent_price=15000.00,
                     location=locations[11],
                     image_url='https://images.unsplash.com/photo-1600607687920-4e3b3a7c0951',
                     landlord_id=users[2].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Donholm Flat',
                     description='Affordable 2-bedroom flat with balcony and parking',
                     rent_price=28000.00,
                     location=locations[12],
                     image_url='https://images.unsplash.com/photo-1600585154340-be6161a56a0c',
                     landlord_id=users[2].id,
                     available=True,
                     created_at=datetime.now()),

            Property(title='Mombasa Road Penthouse',
                     description='Luxury penthouse with panoramic city views',
                     rent_price=120000.00,
                     location=locations[13],
                     image_url='https://images.unsplash.com/photo-1600585154313-26f490a8c9f9',
                     landlord_id=users[1].id,
                     available=True,
                     created_at=datetime.now()),
        ]

        db.session.add_all(properties)
        db.session.flush()

        #seed Property Images
        property_images = []
        for p in properties:
            property_images.append(PropertyImage(
                property_id=p.id,
                image_url=p.image_url,
                caption=f"Main view of {p.title}",
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ))
            property_images.append(PropertyImage(
                property_id=p.id,
                image_url='https://images.unsplash.com/photo-1586023492125-27b2c045efd7',
                caption=f"Interior view of {p.title}",
                is_primary=False,
                sort_order=2,
                created_at=datetime.now()
            ))

        db.session.add_all(property_images)
        db.session.flush()

        #Seed Property Amenities
        base_amenities = ['wifi', 'parking', 'security', 'water', 'electricity']
        extra_amenities = ['gym', 'pool', 'garden', 'balcony', 'laundry']

        amenities = []
        for p in properties:
            for name in base_amenities:
                amenities.append(PropertyAmenity(
                    property_id=p.id,
                    amenity_name=name,
                    description=f"{name.capitalize()} available",
                    included=True
                ))
            amenities.append(PropertyAmenity(
                property_id=p.id,
                amenity_name=extra_amenities[hash(p.title) % len(extra_amenities)],
                description='Extra amenity included',
                included=True
            ))

        db.session.add_all(amenities)
        db.session.flush()

        #seed Bookings
        bookings = [
            Booking(
                tenant_id=users[2].id,
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

        #Seed Payments
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

        #Seed Reviews
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

        print("✅ Database seeded successfully with 14 properties, images, and amenities!")

if __name__ == '__main__':
    seed_database()
