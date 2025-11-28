import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def create_extra_services():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'meetdelux')]
    
    # Get first hotel
    hotel = await db.hotels.find_one()
    if not hotel:
        print("❌ Hiç otel bulunamadı. Önce otel oluşturun.")
        return
    
    hotel_id = hotel['id']
    print(f"✓ Otel bulundu: {hotel['name']}")
    print(f"  Hotel ID: {hotel_id}")
    
    # Ekstra hizmetler listesi
    extra_services = [
        {
            "name": "Sabah Kahvaltısı",
            "description": "Açık büfe kahvaltı - sıcak ve soğuk içecekler, reçel, peynir çeşitleri, taze meyve",
            "price": 25.0,
            "currency": "TRY",
            "unit": "person",
            "category": "catering",
            "service_type": "breakfast",
            "capacity_per_service": 1,
            "is_available": True
        },
        {
            "name": "Öğle Yemeği (Standart)",
            "description": "2 çorba seçeneği, 4 ana yemek, salata büfesi, tatlı, sınırsız içecek",
            "price": 45.0,
            "currency": "TRY",
            "unit": "person",
            "category": "catering",
            "service_type": "lunch",
            "capacity_per_service": 1,
            "is_available": True
        },
        {
            "name": "Premium Akşam Yemeği",
            "description": "Premium menü - özel çorba, 3 ana yemek seçeneği, özel tatlı, limitsiz içecek servisi",
            "price": 75.0,
            "currency": "TRY",
            "unit": "person",
            "category": "catering",
            "service_type": "dinner",
            "capacity_per_service": 1,
            "is_available": True
        },
        {
            "name": "Kahve Molası",
            "description": "Türk kahvesi, çay çeşitleri, kurabiye, küçük kek ve pasta",
            "price": 15.0,
            "currency": "TRY",
            "unit": "person",
            "category": "refreshment",
            "service_type": "coffee_break",
            "capacity_per_service": 1,
            "is_available": True
        },
        {
            "name": "Havalimanı Transfer (İstanbul Havalimanı)",
            "description": "İstanbul Havalimanı ↔ Otel arası lüks araç transfer hizmeti (4 kişilik)",
            "price": 200.0,
            "currency": "TRY",
            "unit": "trip",
            "category": "transport",
            "service_type": "airport_transfer",
            "duration_minutes": 60,
            "capacity_per_service": 4,
            "is_available": True
        },
        {
            "name": "Şehir İçi Transfer",
            "description": "İstanbul şehir merkezi önemli noktalara transfer hizmeti",
            "price": 120.0,
            "currency": "TRY",
            "unit": "trip",
            "category": "transport",
            "service_type": "city_transfer",
            "duration_minutes": 30,
            "capacity_per_service": 4,
            "is_available": True
        },
        {
            "name": "Projeksiyon ve Ses Sistemi",
            "description": "Full HD projeksiyon, ses sistemi, kablosuz mikrofon (2 adet)",
            "price": 150.0,
            "currency": "TRY",
            "unit": "day",
            "category": "equipment",
            "service_type": "projection_sound",
            "is_available": True
        },
        {
            "name": "LED Ekran Kiralama",
            "description": "Büyük boy LED ekran (3x2m), full HD görüntü, teknik destek dahil",
            "price": 300.0,
            "currency": "TRY",
            "unit": "day",
            "category": "equipment",
            "service_type": "led_screen",
            "is_available": True
        },
        {
            "name": "Profesyonel Fotoğrafçı",
            "description": "Etkinlik fotoğraf çekimi, dijital albüm, USB ile teslim",
            "price": 200.0,
            "currency": "TRY",
            "unit": "hour",
            "category": "service",
            "service_type": "photographer",
            "capacity_per_service": 1,
            "is_available": True
        },
        {
            "name": "Hostess Desteği",
            "description": "Profesyonel hostess, karşılama ve yönlendirme hizmeti",
            "price": 60.0,
            "currency": "TRY",
            "unit": "hour",
            "category": "service",
            "service_type": "hostess_support",
            "capacity_per_service": 1,
            "is_available": True
        }
    ]
    
    created_count = 0
    for service_data in extra_services:
        service_data["id"] = str(uuid.uuid4())
        service_data["hotel_id"] = hotel_id
        service_data["created_at"] = datetime.now(timezone.utc)
        
        await db.extra_services.insert_one(service_data)
        created_count += 1
        print(f"  ✓ {service_data['name']} - {service_data['price']} {service_data['currency']}")
    
    print(f"\n🎉 Toplam {created_count} ekstra hizmet başarıyla oluşturuldu!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_extra_services())
