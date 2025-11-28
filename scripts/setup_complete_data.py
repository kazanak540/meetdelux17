#!/usr/bin/env python3
"""
Complete test data setup script for MeetDelux
Creates admin, hotels, conference rooms, and extra services
"""

import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
import bcrypt

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meetdelux')

# Hotel images (15 different luxury hotels)
HOTEL_IMAGES = [
    "https://images.unsplash.com/photo-1561501900-3701fa6a0864?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBob3RlbHxlbnwwfHx8fDE3NjQyOTcyODB8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBob3RlbHxlbnwwfHx8fDE3NjQyOTcyODB8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBob3RlbHxlbnwwfHx8fDE3NjQyOTcyODB8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1621293954908-907159247fc8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBob3RlbHxlbnwwfHx8fDE3NjQyOTcyODB8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1624800873328-129498d2847a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwxfHxjb25mZXJlbmNlJTIwY2VudGVyfGVufDB8fHx8MTc2NDM0NjI3MXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1624800872504-79cf97b34af4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwyfHxjb25mZXJlbmNlJTIwY2VudGVyfGVufDB8fHx8MTc2NDM0NjI3MXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1748802633639-22f99d0b3a0c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHwzfHxjb25mZXJlbmNlJTIwY2VudGVyfGVufDB8fHx8MTc2NDM0NjI3MXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1672396309399-353d95b114a1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzF8MHwxfHNlYXJjaHw0fHxjb25mZXJlbmNlJTIwY2VudGVyfGVufDB8fHx8MTc2NDM0NjI3MXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1711743266323-5badf42d4797?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwxfHxob3RlbCUyMGV4dGVyaW9yfGVufDB8fHx8MTc2NDM0NjI3N3ww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1607320895054-c5c543e9a069?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwyfHxob3RlbCUyMGV4dGVyaW9yfGVufDB8fHx8MTc2NDM0NjI3N3ww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1536269404660-0a8d4e88bf1b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwzfHxob3RlbCUyMGV4dGVyaW9yfGVufDB8fHx8MTc2NDM0NjI3N3ww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1668480441891-3744c25337a3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHw0fHxob3RlbCUyMGV4dGVyaW9yfGVufDB8fHx8MTc2NDM0NjI3N3ww&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/34931018/pexels-photo-34931018.jpeg",
    "https://images.pexels.com/photos/2774566/pexels-photo-2774566.jpeg",
    "https://images.pexels.com/photos/34958207/pexels-photo-34958207.jpeg"
]

# Conference room images (20 different rooms)
ROOM_IMAGES = [
    # Executive Boardrooms
    "https://images.unsplash.com/photo-1431540015161-0bf868a2d407?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxib2FyZHJvb218ZW58MHx8fHwxNzY0MzQ2MzQ2fDA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1582653291997-079a1c04e5a1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxjb25mZXJlbmNlJTIwcm9vbXxlbnwwfHx8fDE3NjQzNDYzMzR8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1517502884422-41eaead166d4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxjb25mZXJlbmNlJTIwcm9vbXxlbnwwfHx8fDE3NjQzNDYzMzR8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1497366811353-6870744d04b2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHw0fHxib2FyZHJvb218ZW58MHx8fHwxNzY0MzQ2MzQ2fDA&ixlib=rb-4.1.0&q=85",
    # Medium Conference Rooms
    "https://images.unsplash.com/photo-1571624436279-b272aff752b5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxjb25mZXJlbmNlJTIwcm9vbXxlbnwwfHx8fDE3NjQzNDYzMzR8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1744095407215-66e40734e23a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwxfHxtZWV0aW5nJTIwaGFsbHxlbnwwfHx8fDE3NjQzNDYzNDB8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1573167507387-6b4b98cb7c13?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwzfHxib2FyZHJvb218ZW58MHx8fHwxNzY0MzQ2MzQ2fDA&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/2976970/pexels-photo-2976970.jpeg",
    # Large Event Halls
    "https://images.unsplash.com/photo-1759477274116-e3cb02d2b9d8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHw0fHxtZWV0aW5nJTIwaGFsbHxlbnwwfHx8fDE3NjQzNDYzNDB8MA&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/159213/hall-congress-architecture-building-159213.jpeg",
    "https://images.pexels.com/photos/269140/pexels-photo-269140.jpeg",
    "https://images.pexels.com/photos/416320/pexels-photo-416320.jpeg",
    # Theater-Style Auditoriums
    "https://images.unsplash.com/photo-1596522354195-e84ae3c98731?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwxfHxhdWRpdG9yaXVtfGVufDB8fHx8MTc2NDM0NjM1M3ww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxhdWRpdG9yaXVtfGVufDB8fHx8MTc2NDM0NjM1M3ww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1594122230689-45899d9e6f69?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwzfHxhdWRpdG9yaXVtfGVufDB8fHx8MTc2NDM0NjM1M3ww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1606761568499-6d2451b23c66?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw0fHxhdWRpdG9yaXVtfGVufDB8fHx8MTc2NDM0NjM1M3ww&ixlib=rb-4.1.0&q=85",
    # Classroom-Style
    "https://images.pexels.com/photos/3864594/pexels-photo-3864594.jpeg",
    "https://images.pexels.com/photos/14501973/pexels-photo-14501973.jpeg",
    "https://images.unsplash.com/photo-1628062699790-7c45262b82b4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxjb25mZXJlbmNlJTIwcm9vbXxlbnwwfHx8fDE3NjQzNDYzMzR8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1698904087385-6b36002264a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDN8MHwxfHNlYXJjaHwzfHxtZWV0aW5nJTIwaGFsbHxlbnwwfHx8fDE3NjQzNDYzNDB8MA&ixlib=rb-4.1.0&q=85"
]

# Hotel data with Turkish cities
HOTELS_DATA = [
    {
        "name": "Grand Horizon Hotel & Conference Center",
        "city": "İstanbul",
        "address": "Levent Mahallesi, Büyükdere Caddesi No:127, Şişli",
        "description": "İstanbul'un kalbinde, lüks konaklama ve dünya standartlarında konferans salonları. 2000 kişilik ana balo salonu, 15 adet toplantı odası ve özel etkinlik alanları.",
        "phone": "+90 212 123 45 67",
        "email": "info@grandhorizon.com.tr",
        "star_rating": 5,
        "facilities": ["Ücretsiz WiFi", "Otopark", "Havalimanı Transferi", "24/7 Resepsiyon", "Spa & Wellness", "Fitness Center", "Restaurant & Bar"]
    },
    {
        "name": "Aegean Business Resort",
        "city": "İzmir",
        "address": "Alsancak Mahallesi, Kıbrıs Şehitleri Caddesi, Konak",
        "description": "Ege'nin incisi İzmir'de, deniz manzaralı konferans salonları ve lüks konaklama imkanları. Modern teknik altyapı ve profesyonel hizmet anlayışı.",
        "phone": "+90 232 456 78 90",
        "email": "rezervasyon@aegeanresort.com.tr",
        "star_rating": 5,
        "facilities": ["Deniz Manzarası", "Ücretsiz WiFi", "Özel Plaj", "Spa", "3 Restaurant", "Pool Bar", "Otopark"]
    },
    {
        "name": "Anatolian Palace Hotel",
        "city": "Ankara",
        "address": "Çankaya, Atatürk Bulvarı No:183",
        "description": "Başkentin merkezinde, devlet protokolü standartlarında hizmet. Yüksek güvenlikli etkinlikler için ideal. VIP toplantı odaları ve geniş balo salonları.",
        "phone": "+90 312 234 56 78",
        "email": "iletisim@anatolianpalace.com.tr",
        "star_rating": 5,
        "facilities": ["VIP Güvenlik", "Simultane Çeviri", "LED Ekran", "Protokol Servisi", "Helipad", "Executive Lounge"]
    },
    {
        "name": "Mediterranean Pearl Resort",
        "city": "Antalya",
        "address": "Lara Plajı, Muratpaşa",
        "description": "Akdeniz'in eşsiz güzelliğinde, all-inclusive konferans paketi. Açık hava etkinlik alanları, sahil konferans salonu ve 5 farklı etkinlik mekanı.",
        "phone": "+90 242 345 67 89",
        "email": "booking@medpearl.com.tr",
        "star_rating": 5,
        "facilities": ["Sahil Etkinlik Alanı", "Açık Havuz", "6 Restaurant", "Aqua Park", "Mini Club", "Heliport"]
    },
    {
        "name": "Black Sea Summit Hotel",
        "city": "Trabzon",
        "address": "Ortahisar, Kunduracılar Caddesi",
        "description": "Karadeniz'in incisi Trabzon'da, dağ ve deniz manzaralı toplantı mekanları. Bölgesel lezzetler ve misafirperverlik bir arada.",
        "phone": "+90 462 567 89 01",
        "email": "info@blackseasummit.com.tr",
        "star_rating": 4,
        "facilities": ["Dağ Manzarası", "Karadeniz Mutfağı", "Spa", "Toplantı Odaları", "Otopark", "Transfer"]
    },
    {
        "name": "Cappadocia Cave Congress Center",
        "city": "Nevşehir",
        "address": "Göreme Mahallesi, Müze Caddesi",
        "description": "Dünya mirası Kapadokya'da, mağara otel konseptinde konferans deneyimi. Eşsiz atmosfer ve unutulmaz etkinlikler için ideal.",
        "phone": "+90 384 678 90 12",
        "email": "reservation@cappadociacave.com.tr",
        "star_rating": 5,
        "facilities": ["Mağara Odalar", "Balon Turu", "Panoramik Terrace", "Türk Hamamı", "Wine Cellar", "Outdoor Events"]
    },
    {
        "name": "Marmara Business Plaza",
        "city": "Bursa",
        "address": "Osmangazi, Fethiye Caddesi No:45",
        "description": "Yeşil Bursa'nın merkezinde, modern iş merkezi oteli. Günübirlik seminer ve toplantılar için pratik lokasyon ve hızlı servis.",
        "phone": "+90 224 789 01 23",
        "email": "info@marmaraplaza.com.tr",
        "star_rating": 4,
        "facilities": ["Şehir Merkezi", "Express Check-in", "Business Lounge", "Meeting Pods", "Teleferik", "Termal"]
    },
    {
        "name": "Pamukkale Thermal Congress Resort",
        "city": "Denizli",
        "address": "Pamukkale Mahallesi, Traverteni Caddesi",
        "description": "Doğal termal kaynaklı spa ve konferans merkezi. Sağlık turizmi ile iş turizmini birleştiren benzersiz konsept.",
        "phone": "+90 258 890 12 34",
        "email": "rezervasyon@pamukkaleresort.com.tr",
        "star_rating": 5,
        "facilities": ["Termal Havuzlar", "Medical Spa", "Golf Course", "Outdoor Conference", "Helipad", "Observatory"]
    },
    {
        "name": "Southeastern Business Hotel",
        "city": "Gaziantep",
        "address": "Şehitkamil, İncilipınar Mahallesi",
        "description": "Gastronomi başkenti Gaziantep'te, yerel kültür ve modern iş imkanları. Bölgesel tatlar eşliğinde etkinlikler.",
        "phone": "+90 342 901 23 45",
        "email": "contact@sebhotel.com.tr",
        "star_rating": 4,
        "facilities": ["Gastronomi Turları", "Mutfak Workshopları", "Rooftop Lounge", "City View", "Otopark", "Transfer"]
    },
    {
        "name": "Aegean Paradise Resort & Spa",
        "city": "Bodrum",
        "address": "Gümbet Mahallesi, Sahil Yolu",
        "description": "Ege'nin en gözde tatil beldesi Bodrum'da, lüks konaklama ve etkinlik mekanları. Marina manzarası ve özel beach club.",
        "phone": "+90 252 012 34 56",
        "email": "info@aegeanparadise.com.tr",
        "star_rating": 5,
        "facilities": ["Private Beach", "Marina", "Yacht Services", "Water Sports", "Night Club", "5 Restaurants"]
    },
    {
        "name": "Central Anatolia Plaza",
        "city": "Konya",
        "address": "Meram, Yeni İstanbul Caddesi No:234",
        "description": "Kültür başkenti Konya'da, tarihi dokuya saygılı modern konferans merkezi. Kültürel etkinlikler için özel programlar.",
        "phone": "+90 332 123 45 67",
        "email": "bilgi@centralplaza.com.tr",
        "star_rating": 4,
        "facilities": ["Kültür Turları", "Mevlana Museum", "Traditional Restaurant", "Prayer Room", "Library", "Garden"]
    },
    {
        "name": "Sky Tower Business Hotel",
        "city": "İstanbul",
        "address": "Maslak, Büyükdere Caddesi, Sarıyer",
        "description": "İstanbul'un en yüksek iş kulesinde, gökyüzü manzaralı toplantılar. Heliport erişimi ve executive servis.",
        "phone": "+90 212 234 56 78",
        "email": "reservation@skytower.com.tr",
        "star_rating": 5,
        "facilities": ["Heliport", "Sky Lounge", "Panoramic View", "Executive Floors", "Concierge", "Valet"]
    },
    {
        "name": "Uludağ Mountain Resort",
        "city": "Bursa",
        "address": "Uludağ Kayak Merkezi, 2500m",
        "description": "Uludağ zirvesinde, dört mevsim etkinlik mekanı. Kış aylarında kayak sonrası toplantılar, yaz aylarında dağ serin liği.",
        "phone": "+90 224 345 67 89",
        "email": "info@uludagresort.com.tr",
        "star_rating": 4,
        "facilities": ["Ski-in/Ski-out", "Mountain View", "Fireplace Lounge", "Wellness", "Adventure Tours", "Cable Car"]
    },
    {
        "name": "Bosphorus Crown Hotel",
        "city": "İstanbul",
        "address": "Beşiktaş, Barbaros Bulvarı No:567",
        "description": "Boğaz manzaralı lüks otel, tarihi yarımada ve modern İstanbul'u birleştiren lokasyon. Gala yemekleri ve özel etkinlikler için tercih edilen mekan.",
        "phone": "+90 212 456 78 90",
        "email": "events@bosphoruscrown.com.tr",
        "star_rating": 5,
        "facilities": ["Bosphorus View", "Yacht Pier", "Rooftop Restaurant", "Spa", "Art Gallery", "Turkish Bath"]
    },
    {
        "name": "Taurus Mountain Lodge",
        "city": "Adana",
        "address": "Seyhan, Ziyapaşa Bulvarı",
        "description": "Toros Dağları eteğinde, doğa ile iç içe konferans deneyimi. Team building aktiviteleri ve outdoor etkinlikler için ideal.",
        "phone": "+90 322 567 89 01",
        "email": "rezervasyon@tauruslodge.com.tr",
        "star_rating": 4,
        "facilities": ["Mountain Activities", "Trekking", "BBQ Area", "Bonfire", "Nature Tours", "Organic Farm"]
    }
]


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def create_admin_user(db):
    """Create admin user"""
    print("\n🔑 Creating admin user...")
    
    admin_email = "admin@meetdelux.com"
    existing = await db.users.find_one({"email": admin_email})
    
    if existing:
        print(f"   ✅ Admin user already exists: {admin_email}")
        return existing["id"]
    
    admin_data = {
        "id": str(uuid.uuid4()),
        "email": admin_email,
        "password": hash_password("admin123"),
        "full_name": "MeetDelux Admin",
        "phone": "+90 535 243 96 96",
        "role": "admin",
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
        "email_verified": True
    }
    
    await db.users.insert_one(admin_data)
    print(f"   ✅ Admin created: {admin_email} / Password: admin123")
    return admin_data["id"]


async def create_hotel_managers(db, count=15):
    """Create hotel manager users"""
    print(f"\n👥 Creating {count} hotel managers...")
    manager_ids = []
    
    for i in range(count):
        email = f"hotel{i+1}@meetdelux.com"
        existing = await db.users.find_one({"email": email})
        
        if existing:
            manager_ids.append(existing["id"])
            continue
        
        manager_data = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password": hash_password("hotel123"),
            "full_name": f"Hotel Manager {i+1}",
            "phone": f"+90 5{i:02d} {i:03d} {i:02d} {i:02d}",
            "role": "hotel_manager",
            "created_at": datetime.now(timezone.utc),
            "is_active": True,
            "email_verified": True
        }
        
        await db.users.insert_one(manager_data)
        manager_ids.append(manager_data["id"])
    
    print(f"   ✅ Created {len(manager_ids)} hotel managers")
    return manager_ids


async def create_hotels(db, manager_ids):
    """Create hotels with different images"""
    print("\n🏨 Creating 15 luxury hotels...")
    hotel_ids = []
    
    for i, hotel_data in enumerate(HOTELS_DATA):
        existing = await db.hotels.find_one({"name": hotel_data["name"]})
        if existing:
            hotel_ids.append(existing["id"])
            continue
        
        hotel = {
            "id": str(uuid.uuid4()),
            "manager_id": manager_ids[i],
            "name": hotel_data["name"],
            "description": hotel_data["description"],
            "address": hotel_data["address"],
            "city": hotel_data["city"],
            "phone": hotel_data["phone"],
            "email": hotel_data["email"],
            "website": f"www.{hotel_data['name'].lower().replace(' ', '')}.com.tr",
            "star_rating": hotel_data["star_rating"],
            "facilities": hotel_data["facilities"],
            "images": [HOTEL_IMAGES[i]],  # Each hotel gets unique image
            "latitude": 41.0082 + (i * 0.1),  # Mock coordinates
            "longitude": 28.9784 + (i * 0.1),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "is_active": True,
            "approval_status": "approved",  # Auto-approve for demo
            "average_rating": 4.5 + (i % 5) * 0.1,
            "total_reviews": 10 + (i * 5)
        }
        
        await db.hotels.insert_one(hotel)
        hotel_ids.append(hotel["id"])
        print(f"   ✅ {hotel['name']} ({hotel['city']})")
    
    return hotel_ids


async def create_conference_rooms(db, hotel_ids):
    """Create 3-5 conference rooms for each hotel"""
    print("\n🎯 Creating conference rooms for each hotel...")
    
    room_types = [
        {
            "name": "Grand Ballroom",
            "type": "ballroom",
            "capacity": 500,
            "area": 800,
            "price_day": 5000,
            "price_hour": 650,
            "features": ["Projeksiyon", "Ses Sistemi", "Sahne", "LED Ekran", "Klima", "WiFi", "Simultane Çeviri"]
        },
        {
            "name": "Executive Boardroom",
            "type": "boardroom",
            "capacity": 30,
            "area": 80,
            "price_day": 800,
            "price_hour": 120,
            "features": ["Projeksiyon", "Whiteboard", "Video Konferans", "Klima", "WiFi", "Coffee Station"]
        },
        {
            "name": "Meeting Room Premium",
            "type": "meeting",
            "capacity": 50,
            "area": 120,
            "price_day": 1200,
            "price_hour": 180,
            "features": ["Projeksiyon", "Ses Sistemi", "Beyaz Tahta", "Klima", "WiFi", "Catering Area"]
        },
        {
            "name": "Conference Hall",
            "type": "conference",
            "capacity": 200,
            "area": 300,
            "price_day": 3000,
            "price_hour": 420,
            "features": ["Projeksiyon", "Ses Sistemi", "Sahne", "Klima", "WiFi", "Backstage", "Green Room"]
        },
        {
            "name": "Training Center",
            "type": "training",
            "capacity": 80,
            "area": 150,
            "price_day": 1500,
            "price_hour": 220,
            "features": ["Projeksiyon", "Whiteboard", "Flipchart", "Klima", "WiFi", "Breakout Rooms"]
        }
    ]
    
    layouts = [
        ["Theater", "Classroom", "U-Shape", "Boardroom"],
        ["Boardroom", "U-Shape"],
        ["Theater", "Classroom", "Boardroom", "Banquet"],
        ["Theater", "Classroom", "U-Shape"],
        ["Classroom", "U-Shape", "Groups"]
    ]
    
    room_count = 0
    room_image_idx = 0
    
    for hotel_id in hotel_ids:
        hotel = await db.hotels.find_one({"id": hotel_id})
        num_rooms = 3 + (hash(hotel_id) % 3)  # 3-5 rooms per hotel
        
        for i in range(num_rooms):
            room_template = room_types[i % len(room_types)]
            
            room = {
                "id": str(uuid.uuid4()),
                "hotel_id": hotel_id,
                "name": f"{room_template['name']} {chr(65+i)}",
                "description": f"{hotel['name']} bünyesindeki {room_template['capacity']} kişilik {room_template['type']} salonu. Modern teknik donanım ve profesyonel hizmet.",
                "capacity": room_template["capacity"],
                "area_sqm": room_template["area"],
                "price_per_day": room_template["price_day"],
                "price_per_hour": room_template["price_hour"],
                "currency": "EUR",
                "room_type": room_template["type"],
                "features": room_template["features"],
                "layout_options": layouts[i % len(layouts)],
                "images": [ROOM_IMAGES[room_image_idx % len(ROOM_IMAGES)]],
                "is_available": True,
                "created_at": datetime.now(timezone.utc),
                "approval_status": "approved",
                "average_rating": 4.3 + (i * 0.15),
                "total_bookings": 5 + (i * 3)
            }
            
            await db.conference_rooms.insert_one(room)
            room_count += 1
            room_image_idx += 1
    
    print(f"   ✅ Created {room_count} conference rooms")


async def create_extra_services(db, hotel_ids):
    """Create extra services for each hotel"""
    print("\n🍽️ Creating extra services for each hotel...")
    
    service_count = 0
    
    for hotel_id in hotel_ids:
        # Use the default services creation logic from backend
        default_services = [
            # Catering
            {"name": "Sabah Kahvaltısı", "price": 15.0, "unit": "person", "category": "catering", "service_type": "breakfast"},
            {"name": "Öğle Yemeği", "price": 28.0, "unit": "person", "category": "catering", "service_type": "lunch"},
            {"name": "Akşam Yemeği", "price": 40.0, "unit": "person", "category": "catering", "service_type": "dinner"},
            {"name": "Kahve Molası", "price": 8.0, "unit": "person", "category": "refreshment", "service_type": "coffee_break"},
            # Services
            {"name": "Hostes Desteği", "price": 25.0, "unit": "hour", "category": "service", "service_type": "hostess_support"},
            {"name": "Teknik Destek", "price": 35.0, "unit": "hour", "category": "service", "service_type": "technical_support"},
            # Transport
            {"name": "Havalimanı Transfer", "price": 80.0, "unit": "trip", "category": "transport", "service_type": "airport_transfer"},
            {"name": "Şehir İçi Transfer", "price": 50.0, "unit": "trip", "category": "transport", "service_type": "city_transfer"},
        ]
        
        for service_data in default_services:
            existing = await db.extra_services.find_one({
                "hotel_id": hotel_id,
                "name": service_data["name"]
            })
            
            if not existing:
                service = {
                    "id": str(uuid.uuid4()),
                    "hotel_id": hotel_id,
                    "name": service_data["name"],
                    "description": f"Profesyonel {service_data['name']} hizmeti",
                    "price": service_data["price"],
                    "currency": "EUR",
                    "unit": service_data["unit"],
                    "category": service_data["category"],
                    "service_type": service_data["service_type"],
                    "is_available": True,
                    "created_at": datetime.now(timezone.utc)
                }
                
                await db.extra_services.insert_one(service)
                service_count += 1
    
    print(f"   ✅ Created {service_count} extra services")


async def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🚀 MeetDelux Complete Test Data Setup")
    print("="*60)
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # 1. Create admin user
        admin_id = await create_admin_user(db)
        
        # 2. Create hotel managers
        manager_ids = await create_hotel_managers(db, count=15)
        
        # 3. Create hotels
        hotel_ids = await create_hotels(db, manager_ids)
        
        # 4. Create conference rooms
        await create_conference_rooms(db, hotel_ids)
        
        # 5. Create extra services
        await create_extra_services(db, hotel_ids)
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print("\n📋 Login Credentials:")
        print("   Admin: admin@meetdelux.com / admin123")
        print("   Hotel Managers: hotel1@meetdelux.com / hotel123")
        print("                   hotel2@meetdelux.com / hotel123")
        print("                   ... (hotel1-15)")
        print("\n🎯 Summary:")
        print(f"   ✅ 1 Admin user")
        print(f"   ✅ 15 Hotel managers")
        print(f"   ✅ 15 Luxury hotels (all approved)")
        print(f"   ✅ 45-75 Conference rooms")
        print(f"   ✅ 120+ Extra services")
        print("\n🌐 You can now browse hotels at: http://localhost:3000/hotels")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
