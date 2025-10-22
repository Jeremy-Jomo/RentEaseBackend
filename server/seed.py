# seed.py
from app import create_app, db
from app.models import User, Property, PropertyImage, PropertyAmenity, Booking, Payment, Review, Favorite, Notification
from datetime import datetime, timedelta
import random

def seed_database():
    """Seed the database with initial data"""
    app = create_app()
    
    with app.app_context():
        
        db.session.query(Notification).delete()
        db.session.query(Favorite).delete()
        db.session.query(Review).delete()
        db.session.query(Payment).delete()
        db.session.query(Booking).delete()
        db.session.query(PropertyAmenity).delete()
        db.session.query(PropertyImage).delete()
        db.session.query(Property).delete()
        db.session.query(User).delete()
        
        
        users = [
            User(
                name='Admin User',
                email='admin@rentease.com',
                password='hashed_password123',
                role='admin',
                created_at=datetime.now()
            ),
            User(
                name='Jeremy Jomo',
                email='jomo.kamau@gmail.com',
                password='hashed_password123',
                role='landlord',
                created_at=datetime.now()
            ),
            User(
                name='Sharon Irungu ',
                email='sharon.irungu@gmail.com',
                password='hashed_password123',
                role='landlord',
                created_at=datetime.now()
            ),
            User(
                name='Esther Mumira ',
                email='esther.mumira@gmail.com',
                password='hashed_password123',
                role='tenant',
                created_at=datetime.now()
            ),
            User(
                name='Mourice Karia ',
                email='morriskaria542@gmail.com',
                password='hashed_password123',
                role='tenant',
                created_at=datetime.now()
            ),
            User(
                name='James Mwangi',
                email='james.mwangi@email.com',
                password='hashed_password123',
                role='tenant',
                created_at=datetime.now()
            )
        ]
        
        for user in users:
            db.session.add(user)
        db.session.flush()  # This assigns IDs to the user objects
        
       
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
                image_url='https://example.com/images/property1.jpg',
                landlord_id=users[1].id,  # John Kamau
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Spacious Karen House',
                description='3-bedroom family house with garden',
                rent_price=85000.00,
                location=locations[2],
                image_url='https://example.com/images/property2.jpg',
                landlord_id=users[1].id,  # John Kamau
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Kilimani Studio',
                description='Cozy studio apartment near amenities',
                rent_price=25000.00,
                location=locations[1],
                image_url='https://example.com/images/property3.jpg',
                landlord_id=users[2].id,  # Mary Wanjiku
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Lavington Bungalow',
                description='Classic 2-bedroom bungalow',
                rent_price=65000.00,
                location=locations[3],
                image_url='https://example.com/images/property4.jpg',
                landlord_id=users[2].id,  # Mary Wanjiku
                available=True,
                created_at=datetime.now()
            ),
            Property(
                title='Kileleshwa Apartment',
                description='Modern 1-bedroom with balcony',
                rent_price=35000.00,
                location=locations[4],
                image_url='https://example.com/images/property5.jpg',
                landlord_id=users[1].id,  # John Kamau
                available=False,
                created_at=datetime.now()
            )
        ]
        
        for property in properties:
            db.session.add(property)
        db.session.flush()
        
        # Seed Property Images
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
                property_id=properties[0].id,
                image_url='https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
                caption='Modern kitchen area',
                is_primary=False,
                sort_order=3,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[1].id,
                image_url='https://images.unsplash.com/photo-1518780664697-55e3ad937233',
                caption='Beautiful exterior of Karen house',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[1].id,
                image_url='https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e',
                caption='Spacious garden and outdoor area',
                is_primary=False,
                sort_order=2,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[1].id,
                image_url='https://images.unsplash.com/photo-1615529328331-f8917597711f',
                caption='Elegant dining room',
                is_primary=False,
                sort_order=3,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[2].id,
                image_url='https://images.unsplash.com/photo-1522708323590-d24dbb6b0267',
                caption='Compact studio living space',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[2].id,
                image_url='https://images.unsplash.com/photo-1554995207-c18c203602cb',
                caption='Modern studio kitchenette',
                is_primary=False,
                sort_order=2,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[2].id,
                image_url='https://images.unsplash.com/photo-1502672260266-1c1ef2d93688',
                caption='Studio bathroom',
                is_primary=False,
                sort_order=3,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[3].id,
                image_url='https://images.unsplash.com/photo-1570129477492-45c003edd2be',
                caption='Classic bungalow exterior',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[3].id,
                image_url='https://images.unsplash.com/photo-1449247709967-d4461a6a6103',
                caption='Cozy bungalow living room',
                is_primary=False,
                sort_order=2,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[3].id,
                image_url='https://images.unsplash.com/photo-1588046130717-0eb1c9a169ba',
                caption='Beautiful garden area',
                is_primary=False,
                sort_order=3,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[4].id,
                image_url='https://images.unsplash.com/photo-1484154218962-a197022b5858',
                caption='Modern apartment with balcony',
                is_primary=True,
                sort_order=1,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[4].id,
                image_url='https://images.unsplash.com/photo-1598928506311-c55ded91a20c',
                caption='Contemporary bedroom',
                is_primary=False,
                sort_order=2,
                created_at=datetime.now()
            ),
            PropertyImage(
                property_id=properties[4].id,
                image_url='https://images.unsplash.com/photo-1556909114-f6e7ad7d3136',
                caption='Well-equipped kitchen',
                is_primary=False,
                sort_order=3,
                created_at=datetime.now()
            )
        ]
        
        for image in property_images:
            db.session.add(image)
        
       
        amenities = [
            PropertyAmenity(
                property_id=properties[0].id,
                amenity_name='wifi',
                description='High-speed internet',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[0].id,
                amenity_name='parking',
                description='Secure parking space',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[0].id,
                amenity_name='air_conditioning',
                description='AC in all rooms',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[1].id,
                amenity_name='parking',
                description='Double parking',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[1].id,
                amenity_name='pool',
                description='Shared swimming pool',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[2].id,
                amenity_name='wifi',
                description='Fiber internet',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[3].id,
                amenity_name='gym',
                description='Access to gym',
                included=True
            ),
            PropertyAmenity(
                property_id=properties[3].id,
                amenity_name='parking',
                description='Street parking',
                included=True
            )
        ]
        
        for amenity in amenities:
            db.session.add(amenity)
        
        # Seed Bookings
        bookings = [
            Booking(
                tenant_id=users[3].id, 
                property_id=properties[0].id,
                start_date=datetime(2024, 1, 15),
                end_date=datetime(2024, 12, 15),
                status='approved',
                created_at=datetime.now()
            ),
            Booking(
                tenant_id=users[4].id,  
                property_id=properties[1].id,
                start_date=datetime(2024, 2, 1),
                end_date=datetime(2025, 1, 31),
                status='approved',
                created_at=datetime.now()
            ),
            Booking(
                tenant_id=users[5].id,  
                property_id=properties[2].id,
                start_date=datetime(2024, 3, 1),
                end_date=datetime(2024, 8, 31),
                status='pending',
                created_at=datetime.now()
            ),
            Booking(
                tenant_id=users[3].id,  
                property_id=properties[3].id,
                start_date=datetime(2024, 1, 20),
                end_date=datetime(2024, 6, 20),
                status='cancelled',
                created_at=datetime.now()
            )
        ]
        
        for booking in bookings:
            db.session.add(booking)
        db.session.flush()  
        
        # Seed Payments
        payments = [
            Payment(
                booking_id=bookings[0].id,
                tenant_id=users[3].id, 
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
                tenant_id=users[4].id,  
                landlord_id=users[2].id,  # Mary Wanjiku
                amount=85000.00,
                payment_method='digital_wallet',
                status='completed',
                transaction_id='TXN00123457',
                paid_at=datetime.now(),
                created_at=datetime.now()
            ),
            Payment(
                booking_id=bookings[2].id,
                tenant_id=users[5].id,  
                landlord_id=users[1].id,  
                amount=25000.00,
                payment_method='credit_card',
                status='pending',
                transaction_id='TXN00123458',
                paid_at=None,
                created_at=datetime.now()
            )
        ]
        
        for payment in payments:
            db.session.add(payment)
        db.session.flush()  
        
        
        reviews = [
            Review(
                booking_id=bookings[0].id,
                tenant_id=users[3].id,  
                property_id=properties[0].id,
                landlord_id=users[1].id,  
                rating=5,
                review_text='Great apartment! The location in Westlands is perfect and the landlord is very responsive.',
                landlord_reply='Thank you for your kind words!',
                is_approved=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Review(
                booking_id=bookings[1].id,
                tenant_id=users[4].id,  
                property_id=properties[1].id,
                landlord_id=users[2].id,
                rating=4,
                review_text='Beautiful house in Karen. Love the garden space!',
                landlord_reply="We're glad you're enjoying the property!",
                is_approved=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        for review in reviews:
            db.session.add(review)
        
        # Seed Favorites
        favorites = [
            Favorite(
                user_id=users[3].id,  
                property_id=properties[1].id,  
                created_at=datetime.now()
            ),
            Favorite(
                user_id=users[4].id,  
                property_id=properties[2].id, 
                created_at=datetime.now()
            ),
            Favorite(
                user_id=users[5].id,  
                property_id=properties[0].id, 
                created_at=datetime.now()
            ),
            Favorite(
                user_id=users[3].id,  
                property_id=properties[2].id, 
                created_at=datetime.now()
            )
        ]
        
        for favorite in favorites:
            db.session.add(favorite)
        
        # Seed Notifications
        notifications = [
            Notification(
                user_id=users[1].id,  
                type='booking_request',
                title='New Booking Request',
                message='David Ochieng has requested to book your Westlands apartment',
                email_sent=False,
                email_sent_at=None,
                sendgrid_message_id=None,
                is_read=False,
                related_entity_type='booking',
                related_entity_id=bookings[0].id,
                action_url='/bookings/1',
                created_at=datetime.now()
            ),
            Notification(
                user_id=users[3].id,  
                type='booking_confirmed',
                title='Booking Confirmed',
                message='Your booking for Karen House has been confirmed',
                email_sent=True,
                email_sent_at=datetime.now(),
                sendgrid_message_id='SG123456',
                is_read=False,
                related_entity_type='booking',
                related_entity_id=bookings[1].id,
                action_url='/bookings/2',
                created_at=datetime.now()
            ),
            Notification(
                user_id=users[2].id,  #
                type='payment_received',
                title='Payment Received',
                message='Payment of KES 85,000 received from Grace Akinyi',
                email_sent=False,
                email_sent_at=None,
                sendgrid_message_id=None,
                is_read=False,
                related_entity_type='payment',
                related_entity_id=payments[1].id,
                action_url='/payments/2',
                created_at=datetime.now()
            )
        ]
        
        for notification in notifications:
            db.session.add(notification)
        
        # Commit all changes
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()