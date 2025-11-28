import asyncio
import bcrypt
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def create_admin():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'meetdelux')]
    
    # Check if admin already exists
    existing_admin = await db.users.find_one({"email": "admin@meetdelux.com"})
    
    if existing_admin:
        print("✓ Admin kullanıcı zaten mevcut")
        print(f"  Email: {existing_admin['email']}")
        print(f"  Role: {existing_admin['role']}")
        return
    
    # Create admin user
    password = "Admin123!"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    from datetime import datetime, timezone
    
    admin_user = {
        "id": str(uuid.uuid4()),
        "email": "admin@meetdelux.com",
        "password": hashed_password.decode('utf-8'),
        "full_name": "Admin User",
        "role": "admin",
        "phone": "+90 555 000 0000",
        "created_at": datetime.now(timezone.utc)
    }
    
    await db.users.insert_one(admin_user)
    print("✓ Admin kullanıcı başarıyla oluşturuldu!")
    print(f"  Email: admin@meetdelux.com")
    print(f"  Şifre: Admin123!")
    print(f"  Role: admin")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
