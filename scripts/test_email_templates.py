import os
from dotenv import load_dotenv
from pathlib import Path
from email_service import email_service
from datetime import datetime

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

def test_all_email_templates():
    """Test all email templates"""
    test_email = "confirmation@meetdelux.com"  # Send to self for testing
    
    print("Testing Email Templates")
    print("=" * 50)
    
    # 1. Welcome Email
    print("\n1. Testing Welcome Email...")
    result = email_service.send_welcome_email(
        user_email=test_email,
        user_name="Test Kullanıcı",
        verification_token="test-token-123"
    )
    print(f"   {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # 2. Login Notification
    print("\n2. Testing Login Notification...")
    result = email_service.send_login_notification(
        user_email=test_email,
        user_name="Test Kullanıcı",
        login_time=datetime.now(),
        ip_address="192.168.1.1"
    )
    print(f"   {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # 3. Booking Confirmation
    print("\n3. Testing Booking Confirmation...")
    booking_details = {
        'booking_id': 'BK-12345',
        'hotel_name': 'Zorlu Center Otel',
        'room_name': 'Panorama Salonu',
        'date': '15.11.2025',
        'time': '10:00 - 18:00',
        'participants': '50',
        'total_price': '₺15,000'
    }
    result = email_service.send_booking_confirmation(
        user_email=test_email,
        user_name="Test Kullanıcı",
        booking_details=booking_details
    )
    print(f"   {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # 4. Booking Approved
    print("\n4. Testing Booking Approved...")
    result = email_service.send_booking_approved(
        user_email=test_email,
        user_name="Test Kullanıcı",
        booking_details=booking_details
    )
    print(f"   {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # 5. Hotel Approved
    print("\n5. Testing Hotel Approved...")
    result = email_service.send_hotel_approved(
        user_email=test_email,
        user_name="Otel Yöneticisi",
        hotel_name="Zorlu Center Otel"
    )
    print(f"   {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # 6. New Booking to Hotel
    print("\n6. Testing New Booking to Hotel...")
    booking_details_extended = {
        **booking_details,
        'customer_name': 'Test Müşteri',
        'customer_email': 'musteri@test.com',
        'customer_phone': '+90 555 123 4567'
    }
    result = email_service.send_new_booking_to_hotel(
        hotel_email=test_email,
        hotel_name="Zorlu Center Otel",
        booking_details=booking_details_extended
    )
    print(f"   {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # 7. Booking Reminder
    print("\n7. Testing Booking Reminder...")
    booking_with_address = {
        **booking_details,
        'address': 'Zorlu Center, Levazım, Koru Sk. No:2, 34340 Beşiktaş/İstanbul'
    }
    result = email_service.send_booking_reminder(
        user_email=test_email,
        user_name="Test Kullanıcı",
        booking_details=booking_with_address
    )
    print(f"   {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    print("\n" + "=" * 50)
    print("Test tamamlandı! Lütfen email kutunuzu kontrol edin.")
    print(f"Test email'leri gönderildi: {test_email}")

if __name__ == "__main__":
    test_all_email_templates()
