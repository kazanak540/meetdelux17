import asyncio
import uuid
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

async def create_15_hotels():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'meetdelux')]
    
    # Her otel için manager oluştur
    hotels_data = [
        {
            "name": "Grand Horizon İstanbul",
            "description": "Boğaz manzaralı ultra lüks 5 yıldızlı otel. Modern mimari ve geleneksel Türk misafirperverliğinin mükemmel birleşimi.",
            "address": "Beşiktaş, İstanbul",
            "city": "İstanbul",
            "district": "Beşiktaş",
            "rating": 4.9,
            "amenities": ["WiFi", "Otopark", "Restoran", "Bar", "Fitness Center", "Spa", "Concierge", "Terrace"],
            "images": [
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200",
                "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=1200",
                "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200"
            ],
            "rooms": [
                {"name": "Boğaz Panorama Balo Salonu", "capacity": 500, "area": 800, "price_day": 25000, "price_hour": 3500, "type": "balo"},
                {"name": "Executive Konferans Salonu", "capacity": 200, "area": 350, "price_day": 12000, "price_hour": 1800, "type": "konferans"},
                {"name": "VIP Toplantı Odası", "capacity": 50, "area": 120, "price_day": 5000, "price_hour": 800, "type": "toplanti"},
                {"name": "Terrace Meeting Room", "capacity": 80, "area": 150, "price_day": 7000, "price_hour": 1100, "type": "toplanti"}
            ],
            "services": [
                {"name": "Premium Gala Yemeği", "price": 450, "unit": "person", "category": "catering"},
                {"name": "Boğaz Turu Teknesi", "price": 8000, "unit": "trip", "category": "transport"},
                {"name": "Canlı Müzik Grubu", "price": 5000, "unit": "hour", "category": "service"},
                {"name": "Profesyonel Video Çekim", "price": 8000, "unit": "day", "category": "service"},
                {"name": "Kokteyl Bar Servisi", "price": 180, "unit": "person", "category": "refreshment"}
            ]
        },
        {
            "name": "Tarihi Pera Palas",
            "description": "1892'den beri İstanbul'un kalbinde, tarihi dokusuyla eşsiz bir etkinlik mekanı.",
            "address": "Beyoğlu, İstanbul",
            "city": "İstanbul",
            "district": "Beyoğlu",
            "rating": 4.8,
            "amenities": ["WiFi", "Valet", "Restoran", "Bar", "Tarihi Mimari", "Müze", "Kütüphane"],
            "images": [
                "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=1200",
                "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200",
                "https://images.unsplash.com/photo-1519167758481-83f29da8c424?w=1200"
            ],
            "rooms": [
                {"name": "Agatha Christie Balo Salonu", "capacity": 350, "area": 600, "price_day": 20000, "price_hour": 3000, "type": "balo"},
                {"name": "Orient Express Salonu", "capacity": 120, "area": 250, "price_day": 9000, "price_hour": 1400, "type": "konferans"},
                {"name": "Atatürk Toplantı Odası", "capacity": 40, "area": 90, "price_day": 4000, "price_hour": 650, "type": "toplanti"}
            ],
            "services": [
                {"name": "Osmanlı Mutfağı Menü", "price": 380, "unit": "person", "category": "catering"},
                {"name": "Klasik Piyano Eşliği", "price": 3500, "unit": "hour", "category": "service"},
                {"name": "Tarihi Tur Rehberliği", "price": 2000, "unit": "event", "category": "service"},
                {"name": "Vintage Fotoğraf Köşesi", "price": 3000, "unit": "day", "category": "service"}
            ]
        },
        {
            "name": "Ankara Diplomat Hotel",
            "description": "Başkentin prestijli iş merkezi. Devlet protokolü standartlarında hizmet.",
            "address": "Çankaya, Ankara",
            "city": "Ankara",
            "district": "Çankaya",
            "rating": 4.7,
            "amenities": ["WiFi", "Otopark", "Business Center", "Çeviri Hizmeti", "Simultane Tercüme", "Restoran"],
            "images": [
                "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1200",
                "https://images.unsplash.com/photo-1561501900-3701fa6a0864?w=1200",
                "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=1200"
            ],
            "rooms": [
                {"name": "Meclis Konferans Salonu", "capacity": 400, "area": 650, "price_day": 18000, "price_hour": 2800, "type": "konferans"},
                {"name": "Diplomat Balo Salonu", "capacity": 300, "area": 500, "price_day": 16000, "price_hour": 2500, "type": "balo"},
                {"name": "Protocol Toplantı Odası", "capacity": 30, "area": 80, "price_day": 3500, "price_hour": 600, "type": "toplanti"},
                {"name": "Senato Seminer Odası", "capacity": 100, "area": 180, "price_day": 6000, "price_hour": 950, "type": "seminer"}
            ],
            "services": [
                {"name": "Devlet Protokolü Yemek", "price": 320, "unit": "person", "category": "catering"},
                {"name": "Simultane Tercüme Kabini", "price": 4000, "unit": "day", "category": "equipment"},
                {"name": "Güvenlik Detayı", "price": 8000, "unit": "day", "category": "service"},
                {"name": "Basın Yayın Desteği", "price": 5000, "unit": "event", "category": "service"}
            ]
        },
        {
            "name": "Antalya Sunset Resort",
            "description": "Akdeniz'in incisi. Plaj kenarında all-inclusive etkinlik deneyimi.",
            "address": "Lara, Antalya",
            "city": "Antalya",
            "district": "Lara",
            "rating": 4.9,
            "amenities": ["WiFi", "Özel Plaj", "Havuz", "Spa", "Water Sports", "Beach Bar", "Otopark"],
            "images": [
                "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200",
                "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=1200",
                "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200"
            ],
            "rooms": [
                {"name": "Sunset Beach Balo Salonu", "capacity": 600, "area": 900, "price_day": 28000, "price_hour": 4000, "type": "balo"},
                {"name": "Mediterranean Conference Hall", "capacity": 250, "area": 400, "price_day": 14000, "price_hour": 2200, "type": "konferans"},
                {"name": "Poolside Meeting Pavilion", "capacity": 100, "area": 200, "price_day": 7500, "price_hour": 1200, "type": "toplanti"},
                {"name": "Beach Cocktail Area", "capacity": 150, "area": 300, "price_day": 10000, "price_hour": 1600, "type": "kokteyl"}
            ],
            "services": [
                {"name": "Beach BBQ Premium", "price": 420, "unit": "person", "category": "catering"},
                {"name": "Tekne Partisi", "price": 12000, "unit": "event", "category": "transport"},
                {"name": "Su Sporları Aktivite", "price": 8000, "unit": "day", "category": "service"},
                {"name": "Gün Batımı Kokteyl Setup", "price": 6000, "unit": "event", "category": "refreshment"},
                {"name": "DJ ve Sahne Ekipmanı", "price": 7000, "unit": "day", "category": "equipment"}
            ]
        },
        {
            "name": "Uludağ Mountain Lodge",
            "description": "Dağ eteğinde huzur dolu bir etkinlik mekanı. Kış ve yaz etkinlikleri için ideal.",
            "address": "Uludağ, Bursa",
            "city": "Bursa",
            "district": "Uludağ",
            "rating": 4.6,
            "amenities": ["WiFi", "Şömine", "Terrace", "Spa", "Doğa Yürüyüşü", "Kayak", "Restoran"],
            "images": [
                "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1200",
                "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1200",
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200"
            ],
            "rooms": [
                {"name": "Alpine Grand Hall", "capacity": 250, "area": 450, "price_day": 15000, "price_hour": 2300, "type": "balo"},
                {"name": "Mountain View Conference", "capacity": 150, "area": 280, "price_day": 9000, "price_hour": 1400, "type": "konferans"},
                {"name": "Fireside Meeting Room", "capacity": 50, "area": 100, "price_day": 4500, "price_hour": 750, "type": "toplanti"},
                {"name": "Terrace Seminar Space", "capacity": 80, "area": 160, "price_day": 6000, "price_hour": 950, "type": "seminer"}
            ],
            "services": [
                {"name": "Dağ Kahvaltısı Büfesi", "price": 180, "unit": "person", "category": "catering"},
                {"name": "Teleferik Transfer", "price": 3000, "unit": "group", "category": "transport"},
                {"name": "Doğa Yürüyüşü Guide", "price": 2500, "unit": "day", "category": "service"},
                {"name": "Kış Sporları Ekipman", "price": 5000, "unit": "day", "category": "equipment"}
            ]
        },
        {
            "name": "Château de İzmir",
            "description": "Fransız şatosu mimarisi. Üzüm bağları arasında romantik etkinlikler.",
            "address": "Urla, İzmir",
            "city": "İzmir",
            "district": "Urla",
            "rating": 4.8,
            "amenamenities": ["WiFi", "Şarap Mahzeni", "Bahçe", "Şapel", "Havuz", "Valet", "Restoran"],
            "images": [
                "https://images.unsplash.com/photo-1519167758481-83f29da8c424?w=1200",
                "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=1200",
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200"
            ],
            "rooms": [
                {"name": "Château Grand Ballroom", "capacity": 400, "area": 700, "price_day": 22000, "price_hour": 3200, "type": "balo"},
                {"name": "Wine Cellar Event Space", "capacity": 80, "area": 150, "price_day": 8000, "price_hour": 1300, "type": "kokteyl"},
                {"name": "Garden Pavilion", "capacity": 200, "area": 350, "price_day": 12000, "price_hour": 1900, "type": "konferans"},
                {"name": "Chapel Meeting Room", "capacity": 60, "area": 110, "price_day": 5500, "price_hour": 900, "type": "toplanti"}
            ],
            "services": [
                {"name": "Wine Tasting Event", "price": 250, "unit": "person", "category": "refreshment"},
                {"name": "French Cuisine Premium", "price": 480, "unit": "person", "category": "catering"},
                {"name": "Classical String Quartet", "price": 6000, "unit": "event", "category": "service"},
                {"name": "Garden Wedding Setup", "price": 10000, "unit": "event", "category": "service"}
            ]
        },
        {
            "name": "Bodrum Zen Retreat",
            "description": "Minimalist Japon estetiği ile huzur dolu etkinlik alanı. Ege'nin mavisi eşliğinde.",
            "address": "Yalıkavak, Bodrum",
            "city": "Muğla",
            "district": "Bodrum",
            "rating": 4.7,
            "amenities": ["WiFi", "Yoga Studio", "Meditation Garden", "Organic Cafe", "Spa", "Infinity Pool"],
            "images": [
                "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=1200",
                "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200",
                "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1200"
            ],
            "rooms": [
                {"name": "Zen Grand Hall", "capacity": 200, "area": 400, "price_day": 14000, "price_hour": 2100, "type": "konferans"},
                {"name": "Meditation Circle", "capacity": 100, "area": 180, "price_day": 7000, "price_hour": 1100, "type": "seminer"},
                {"name": "Infinity View Terrace", "capacity": 150, "area": 250, "price_day": 10000, "price_hour": 1600, "type": "kokteyl"},
                {"name": "Tea Ceremony Room", "capacity": 30, "area": 60, "price_day": 3500, "price_hour": 600, "type": "toplanti"}
            ],
            "services": [
                {"name": "Organic Vegan Menu", "price": 280, "unit": "person", "category": "catering"},
                {"name": "Yoga Instructor", "price": 3000, "unit": "session", "category": "service"},
                {"name": "Sound Healing Session", "price": 4000, "unit": "event", "category": "service"},
                {"name": "Japanese Tea Ceremony", "price": 150, "unit": "person", "category": "refreshment"}
            ]
        },
        {
            "name": "İstanbul Loft Factory",
            "description": "Endüstriyel chic tasarım. Yaratıcı ekipler için ilham verici workspace.",
            "address": "Maslak, İstanbul",
            "city": "İstanbul",
            "district": "Maslak",
            "rating": 4.6,
            "amenities": ["High-Speed WiFi", "Podcast Studio", "Green Screen", "Gaming Area", "Coffee Lab"],
            "images": [
                "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200",
                "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1200",
                "https://images.unsplash.com/photo-1600607687644-c7171b42498b?w=1200"
            ],
            "rooms": [
                {"name": "Main Loft Space", "capacity": 300, "area": 550, "price_day": 16000, "price_hour": 2400, "type": "konferans"},
                {"name": "Innovation Lab", "capacity": 80, "area": 150, "price_day": 7000, "price_hour": 1100, "type": "seminer"},
                {"name": "Brainstorm Room", "capacity": 40, "area": 80, "price_day": 4000, "price_hour": 700, "type": "toplanti"},
                {"name": "Rooftop Terrace", "capacity": 120, "area": 200, "price_day": 8500, "price_hour": 1350, "type": "kokteyl"}
            ],
            "services": [
                {"name": "Street Food Catering", "price": 220, "unit": "person", "category": "catering"},
                {"name": "Tech Setup & Support", "price": 5000, "unit": "day", "category": "equipment"},
                {"name": "Live Streaming Package", "price": 6000, "unit": "event", "category": "service"},
                {"name": "Craft Beer Bar", "price": 120, "unit": "person", "category": "refreshment"}
            ]
        },
        {
            "name": "Sultanahmet Palace Hotel",
            "description": "Tarihi yarımadanın kalbinde, Osmanlı saray mimarisi. Kültür ve zarafet buluşması.",
            "address": "Sultanahmet, İstanbul",
            "city": "İstanbul",
            "district": "Fatih",
            "rating": 4.9,
            "amenities": ["WiFi", "Tarihi Hamam", "Osmanlı Bahçesi", "Terrace", "Museum", "Restoran"],
            "images": [
                "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200",
                "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=1200",
                "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=1200"
            ],
            "rooms": [
                {"name": "Imperial Ballroom", "capacity": 450, "area": 750, "price_day": 26000, "price_hour": 3800, "type": "balo"},
                {"name": "Sultanate Conference Hall", "capacity": 180, "area": 320, "price_day": 11000, "price_hour": 1700, "type": "konferans"},
                {"name": "Harem Meeting Suite", "capacity": 50, "area": 100, "price_day": 5500, "price_hour": 900, "type": "toplanti"},
                {"name": "Terrace Garden Event", "capacity": 200, "area": 350, "price_day": 13000, "price_hour": 2000, "type": "kokteyl"}
            ],
            "services": [
                {"name": "Ottoman Palace Cuisine", "price": 520, "unit": "person", "category": "catering"},
                {"name": "Whirling Dervish Show", "price": 8000, "unit": "event", "category": "service"},
                {"name": "Turkish Coffee Fortune", "price": 80, "unit": "person", "category": "refreshment"},
                {"name": "Historical Tour Guide", "price": 3000, "unit": "event", "category": "service"},
                {"name": "Traditional Music Ensemble", "price": 6000, "unit": "event", "category": "service"}
            ]
        },
        {
            "name": "Green Valley Eco Lodge",
            "description": "Doğayla iç içe, sürdürülebilir etkinlik mekanı. Karbon-nötr organizasyonlar için.",
            "address": "Datça, Muğla",
            "city": "Muğla",
            "district": "Datça",
            "rating": 4.7,
            "amenities": ["Solar Power", "Organic Farm", "Composting", "Nature Trails", "Outdoor Cinema"],
            "images": [
                "https://images.unsplash.com/photo-1587061949409-02df41d5e562?w=1200",
                "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1200",
                "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1200"
            ],
            "rooms": [
                {"name": "Eco Grand Pavilion", "capacity": 180, "area": 350, "price_day": 12000, "price_hour": 1850, "type": "konferans"},
                {"name": "Forest Meeting Dome", "capacity": 60, "area": 120, "price_day": 5000, "price_hour": 850, "type": "toplanti"},
                {"name": "Outdoor Amphitheater", "capacity": 250, "area": 500, "price_day": 10000, "price_hour": 1600, "type": "seminer"},
                {"name": "Garden Party Area", "capacity": 150, "area": 280, "price_day": 8000, "price_hour": 1300, "type": "kokteyl"}
            ],
            "services": [
                {"name": "Farm-to-Table Organic", "price": 290, "unit": "person", "category": "catering"},
                {"name": "Eco Workshop Facilitation", "price": 4000, "unit": "day", "category": "service"},
                {"name": "Nature Therapy Session", "price": 2500, "unit": "group", "category": "service"},
                {"name": "Zero-Waste Event Setup", "price": 3000, "unit": "event", "category": "service"}
            ]
        },
        {
            "name": "TechHub Innovation Center",
            "description": "Startuplar ve tech konferansları için next-gen venue. Yapay zeka destekli etkinlik yönetimi.",
            "address": "Levent, İstanbul",
            "city": "İstanbul",
            "district": "Levent",
            "rating": 4.8,
            "amenities": ["10Gbps Internet", "VR Lab", "Maker Space", "Pitch Stage", "Smart Rooms"],
            "images": [
                "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1200",
                "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200",
                "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1200"
            ],
            "rooms": [
                {"name": "Main Stage Arena", "capacity": 500, "area": 800, "price_day": 20000, "price_hour": 3000, "type": "konferans"},
                {"name": "Pitch Deck Theater", "capacity": 200, "area": 350, "price_day": 10000, "price_hour": 1600, "type": "seminer"},
                {"name": "Hackathon Lab", "capacity": 100, "area": 200, "price_day": 8000, "price_hour": 1300, "type": "toplanti"},
                {"name": "Networking Lounge", "capacity": 150, "area": 250, "price_day": 7000, "price_hour": 1150, "type": "kokteyl"}
            ],
            "services": [
                {"name": "Tech Catering & Energy", "price": 180, "unit": "person", "category": "catering"},
                {"name": "Live Coding Challenge", "price": 5000, "unit": "event", "category": "service"},
                {"name": "VR Experience Setup", "price": 8000, "unit": "day", "category": "equipment"},
                {"name": "Mentor Network Access", "price": 3000, "unit": "event", "category": "service"}
            ]
        },
        {
            "name": "Art Deco Nostalji İzmir",
            "description": "1930'ların Art Deco zarafeti. Vintage severlerin gözdesi.",
            "address": "Alsancak, İzmir",
            "city": "İzmir",
            "district": "Konak",
            "rating": 4.7,
            "amenities": ["WiFi", "Vintage Bar", "Jazz Club", "Rooftop", "Antique Furniture", "Photography"],
            "images": [
                "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200",
                "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=1200",
                "https://images.unsplash.com/photo-1519167758481-83f29da8c424?w=1200"
            ],
            "rooms": [
                {"name": "Art Deco Grand Ballroom", "capacity": 300, "area": 550, "price_day": 17000, "price_hour": 2600, "type": "balo"},
                {"name": "Gatsby Meeting Room", "capacity": 80, "area": 150, "price_day": 6500, "price_hour": 1050, "type": "toplanti"},
                {"name": "Jazz Club Lounge", "capacity": 120, "area": 220, "price_day": 8500, "price_hour": 1350, "type": "kokteyl"},
                {"name": "Rooftop Terrace", "capacity": 150, "area": 270, "price_day": 9000, "price_hour": 1450, "type": "seminer"}
            ],
            "services": [
                {"name": "1930s Themed Menu", "price": 350, "unit": "person", "category": "catering"},
                {"name": "Jazz Band Performance", "price": 6000, "unit": "event", "category": "service"},
                {"name": "Vintage Photography", "price": 4000, "unit": "event", "category": "service"},
                {"name": "Classic Cocktail Bar", "price": 160, "unit": "person", "category": "refreshment"}
            ]
        },
        {
            "name": "Futura Space Ankara",
            "description": "Geleceğin etkinlik mekanı. Hologram teknolojisi ve akıllı sistemler.",
            "address": "Bilkent, Ankara",
            "city": "Ankara",
            "district": "Çankaya",
            "rating": 4.9,
            "amenities": ["5G Network", "Hologram Stage", "AI Assistant", "Smart Lighting", "Digital Walls"],
            "images": [
                "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200",
                "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1200",
                "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1200"
            ],
            "rooms": [
                {"name": "Quantum Conference Hall", "capacity": 400, "area": 700, "price_day": 22000, "price_hour": 3300, "type": "konferans"},
                {"name": "Hologram Theater", "capacity": 250, "area": 450, "price_day": 15000, "price_hour": 2350, "type": "seminer"},
                {"name": "AI Innovation Lab", "capacity": 100, "area": 180, "price_day": 9000, "price_hour": 1450, "type": "toplanti"},
                {"name": "Digital Lounge", "capacity": 180, "area": 320, "price_day": 11000, "price_hour": 1750, "type": "kokteyl"}
            ],
            "services": [
                {"name": "Molecular Gastronomy", "price": 420, "unit": "person", "category": "catering"},
                {"name": "Holographic Presentation", "price": 12000, "unit": "event", "category": "equipment"},
                {"name": "AI Event Management", "price": 8000, "unit": "day", "category": "service"},
                {"name": "Interactive Digital Wall", "price": 6000, "unit": "day", "category": "equipment"}
            ]
        },
        {
            "name": "Kapadokya Cave Suites",
            "description": "Peri bacaları arasında mağara otel. Eşsiz doğal akustikte etkinlikler.",
            "address": "Göreme, Nevşehir",
            "city": "Nevşehir",
            "district": "Göreme",
            "rating": 4.9,
            "amenities": ["WiFi", "Cave Spa", "Hot Air Balloon", "Terrace", "Wine Cellar", "Photography"],
            "images": [
                "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1200",
                "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1200",
                "https://images.unsplash.com/photo-1587061949409-02df41d5e562?w=1200"
            ],
            "rooms": [
                {"name": "Grand Cave Ballroom", "capacity": 200, "area": 400, "price_day": 18000, "price_hour": 2750, "type": "balo"},
                {"name": "Valley View Conference", "capacity": 120, "area": 240, "price_day": 10000, "price_hour": 1600, "type": "konferans"},
                {"name": "Fairy Chimney Terrace", "capacity": 80, "area": 160, "price_day": 7500, "price_hour": 1200, "type": "kokteyl"},
                {"name": "Underground Meeting Cave", "capacity": 40, "area": 90, "price_day": 5000, "price_hour": 850, "type": "toplanti"}
            ],
            "services": [
                {"name": "Kapadokya Wine & Dine", "price": 380, "unit": "person", "category": "catering"},
                {"name": "Hot Air Balloon Ride", "price": 15000, "unit": "group", "category": "transport"},
                {"name": "Pottery Workshop", "price": 3000, "unit": "event", "category": "service"},
                {"name": "Sunset Photography Tour", "price": 4000, "unit": "event", "category": "service"},
                {"name": "Traditional Turkish Night", "price": 7000, "unit": "event", "category": "service"}
            ]
        },
        {
            "name": "Marina Bay Convention",
            "description": "Yat limanı manzaralı modern kongre merkezi. Lüks ve prestijin adresi.",
            "address": "Ataköy, İstanbul",
            "city": "İstanbul",
            "district": "Bakırköy",
            "rating": 4.8,
            "amenities": ["WiFi", "Marina View", "Helipad", "Yacht Club", "Fine Dining", "Business Center"],
            "images": [
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200",
                "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200",
                "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=1200"
            ],
            "rooms": [
                {"name": "Marina Grand Ballroom", "capacity": 700, "area": 1000, "price_day": 35000, "price_hour": 5000, "type": "balo"},
                {"name": "Yacht Club Conference", "capacity": 300, "area": 500, "price_day": 18000, "price_hour": 2800, "type": "konferans"},
                {"name": "Captain's Meeting Room", "capacity": 60, "area": 120, "price_day": 6000, "price_hour": 1000, "type": "toplanti"},
                {"name": "Sunset Terrace", "capacity": 200, "area": 350, "price_day": 12000, "price_hour": 1900, "type": "kokteyl"}
            ],
            "services": [
                {"name": "Luxury Seafood Buffet", "price": 550, "unit": "person", "category": "catering"},
                {"name": "Private Yacht Charter", "price": 20000, "unit": "event", "category": "transport"},
                {"name": "Marina Cocktail Party", "price": 250, "unit": "person", "category": "refreshment"},
                {"name": "Helicopter Transfer", "price": 15000, "unit": "trip", "category": "transport"},
                {"name": "VIP Concierge Service", "price": 5000, "unit": "day", "category": "service"}
            ]
        }
    ]
    
    print("🏨 15 Lüks Otel Oluşturuluyor...\n")
    
    for idx, hotel_data in enumerate(hotels_data, 1):
        try:
            # Manager user oluştur
            manager_email = f"manager{idx}@{hotel_data['name'].lower().replace(' ', '')}.com"
            manager_password = f"Manager{idx}23!"
            
            # Check if user exists
            existing_user = await db.users.find_one({"email": manager_email})
            if not existing_user:
                hashed_password = bcrypt.hashpw(manager_password.encode('utf-8'), bcrypt.gensalt())
                user_dict = {
                    "id": str(uuid.uuid4()),
                    "email": manager_email,
                    "password": hashed_password.decode('utf-8'),
                    "full_name": f"{hotel_data['name']} Manager",
                    "role": "hotel_manager",
                    "phone": f"+90 555 {idx:03d} {idx:02d} {idx:02d}",
                    "created_at": datetime.now(timezone.utc),
                    "is_active": True
                }
                await db.users.insert_one(user_dict)
                manager_id = user_dict["id"]
            else:
                manager_id = existing_user["id"]
            
            # Hotel oluştur
            hotel_id = str(uuid.uuid4())
            hotel_dict = {
                "id": hotel_id,
                "manager_id": manager_id,
                "name": hotel_data["name"],
                "description": hotel_data["description"],
                "address": hotel_data["address"],
                "city": hotel_data["city"],
                "district": hotel_data["district"],
                "rating": hotel_data["rating"],
                "amenities": hotel_data["amenities"],
                "images": hotel_data["images"],
                "approval_status": "approved",
                "is_active": True,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
            
            await db.hotels.insert_one(hotel_dict)
            
            # Salonları oluştur
            room_count = 0
            for room_data in hotel_data["rooms"]:
                room_id = str(uuid.uuid4())
                room_dict = {
                    "id": room_id,
                    "hotel_id": hotel_id,
                    "name": room_data["name"],
                    "capacity": room_data["capacity"],
                    "area_sqm": room_data["area"],
                    "price_per_day": room_data["price_day"],
                    "price_per_hour": room_data["price_hour"],
                    "amenities": ["Projeksiyon", "Ses Sistemi", "Klima", "WiFi", "Catering Alanı"],
                    "room_type": room_data["type"],
                    "is_available": True,
                    "approval_status": "approved",
                    "images": hotel_data["images"][:2],
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }
                await db.conference_rooms.insert_one(room_dict)
                room_count += 1
            
            # Ekstra hizmetler oluştur
            service_count = 0
            for service_data in hotel_data["services"]:
                service_id = str(uuid.uuid4())
                service_dict = {
                    "id": service_id,
                    "hotel_id": hotel_id,
                    "name": service_data["name"],
                    "description": f"Premium {service_data['name']} hizmeti",
                    "price": service_data["price"],
                    "currency": "TRY",
                    "unit": service_data["unit"],
                    "category": service_data["category"],
                    "is_available": True,
                    "created_at": datetime.now(timezone.utc)
                }
                await db.extra_services.insert_one(service_dict)
                service_count += 1
            
            print(f"✅ {idx}. {hotel_data['name']}")
            print(f"   📧 Manager: {manager_email} / {manager_password}")
            print(f"   🏛️ {room_count} salon, 💎 {service_count} ekstra hizmet")
            print(f"   📍 {hotel_data['city']}, {hotel_data['district']}\n")
            
        except Exception as e:
            print(f"❌ {hotel_data['name']} oluşturulurken hata: {str(e)}\n")
    
    # Özet
    total_hotels = await db.hotels.count_documents({"approval_status": "approved"})
    total_rooms = await db.conference_rooms.count_documents({"approval_status": "approved"})
    total_services = await db.extra_services.count_documents({})
    
    print("\n" + "="*60)
    print("🎉 TAMAMLANDI!")
    print("="*60)
    print(f"📊 Toplam Onaylı Otel: {total_hotels}")
    print(f"🏛️ Toplam Onaylı Salon: {total_rooms}")
    print(f"💎 Toplam Ekstra Hizmet: {total_services}")
    print("="*60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_15_hotels())
