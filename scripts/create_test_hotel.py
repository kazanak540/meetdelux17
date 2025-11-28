import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def create_test_hotel():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'meetdelux')]
    
    # Create a hotel manager user if not exists
    manager = await db.users.find_one({"email": "manager@test.com"})
    if not manager:
        import bcrypt
        password = "Manager123!"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        manager = {
            "id": str(uuid.uuid4()),
            "email": "manager@test.com",
            "password": hashed_password.decode('utf-8'),
            "full_name": "Test Manager",
            "role": "hotel_manager",
            "phone": "+90 555 111 1111"
        }
        await db.users.insert_one(manager)
        print("✓ Test manager oluşturuldu (manager@test.com / Manager123!)")
    
    # Create a pending hotel
    from datetime import datetime, timezone
    
    test_hotel = {
        "id": str(uuid.uuid4()),
        "name": "Test Oteli - Onay Bekliyor",
        "description": "Bu otel admin onayı beklemektedir. Önizleme ve onaylama özelliğini test etmek için oluşturulmuştur.",
        "address": "Zorlu Center, Levazım, Koru Sk. No:2, 34340 Beşiktaş/İstanbul",
        "city": "İstanbul",
        "phone": "+90 212 924 0000",
        "email": "info@testhotel.com",
        "website": "https://testhotel.com",
        "star_rating": 5,
        "facilities": ["wifi", "parking", "restaurant", "gym", "spa", "business_center"],
        "latitude": "41.0555",
        "longitude": "29.0118",
        "manager_id": manager["id"],
        "images": [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945",
            "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb"
        ],
        "approval_status": "pending",
        "average_rating": 0.0,
        "total_reviews": 0,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    await db.hotels.insert_one(test_hotel)
    print(f"✓ Test oteli oluşturuldu: {test_hotel['name']}")
    print(f"  Status: pending (onay bekliyor)")
    print(f"  ID: {test_hotel['id']}")
    
    # Count pending hotels
    pending_count = await db.hotels.count_documents({"approval_status": "pending"})
    print(f"\n📋 Toplam onay bekleyen otel: {pending_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_hotel())
