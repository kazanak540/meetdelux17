# MeetDelux17 - Seminer & Toplantı Salonu Rezervasyon Platformu

Türkiye'nin en prestijli otellerinde seminer salonu, toplantı salonu ve konferans salonu rezervasyonu için geliştirilmiş **production-ready** platform.

![MeetDelux](https://img.shields.io/badge/Status-Production%20Ready-green)
![Tech](https://img.shields.io/badge/Tech-FastAPI%20%2B%20React-blue)
![Images](https://img.shields.io/badge/Images-Included-orange)

## ✨ Özellikler

### 📦 Tam Paket (Self-Contained)
- ✅ **15 Otel + 60+ Konferans Salonu** (Gerçek fotoğraflarla)
- ✅ **35 Fotoğraf Dahil** (`/frontend/public/images/`)
- ✅ Gmail SMTP E-posta Sistemi
- ✅ Stripe Ödeme Entegrasyonu
- ✅ Dashboard & Analytics API
- ✅ Review & Rating Sistemi
- ✅ SEO Optimizasyonu (Meta tags, Sitemap)
- ✅ Test Coverage (Pytest)
- ✅ Mobil Responsive Tasarım

### 🎯 Teknik Özellikler
- Platform Bypass Koruması
- Multi-image Upload
- Advanced Filtering & Search
- Rezervasyon Takvimi
- Role-based Authentication
- Dashboard Analytics

## 🚀 Hızlı Başlangıç

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/meetdelux17.git
cd meetdelux17
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

**backend/.env** dosyasını yapılandırın (örnek aşağıda)

### 3. Frontend Setup

```bash
cd frontend
yarn install
```

### 4. MongoDB & Database Seed

```bash
# MongoDB'yi başlatın
mongod

# Database'i seed edin (15 otel + fotoğraflar)
cd scripts
python setup_complete_data.py
```

### 5. Run

```bash
# Backend (Terminal 1)
cd backend
python server.py
# → http://localhost:8001

# Frontend (Terminal 2)
cd frontend
yarn start
# → http://localhost:3000
```

## 🔐 Test Kullanıcıları

Database seed sonrası kullanabilirsiniz:

| Rol | Email | Şifre |
|-----|-------|-------|
| **Admin** | admin@meetdelux.com | admin123 |
| **Otel Yöneticisi** | hotel1@meetdelux.com | hotel123 |

## 📁 Proje Yapısı

```
meetdelux17/
├── backend/
│   ├── server.py           # FastAPI (3165 satır)
│   ├── email_service.py    # Gmail SMTP
│   ├── tests/              # Pytest
│   ├── .env                # Config
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── images/
│   │   │   ├── hotels/     # 15 otel fotoğrafı ✅
│   │   │   └── rooms/      # 20 salon fotoğrafı ✅
│   │   ├── sitemap.xml     # SEO
│   │   └── robots.txt      # SEO
│   ├── src/components/     # 30+ React component
│   └── package.json
└── scripts/
    └── setup_complete_data.py  # Database seeding (local images)
```

## 🌐 Environment Variables

### backend/.env
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=meetdelux
JWT_SECRET_KEY=your-secret-key-change-this
APP_URL=http://localhost:3000

# Stripe (Test Mode)
STRIPE_API_KEY=your-stripe-test-key

# Gmail SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=MeetDelux
```

### frontend/.env
```env
REACT_APP_BACKEND_URL=
```

## 📊 Tech Stack

| Kategori | Teknoloji |
|----------|-----------|
| **Backend** | FastAPI, Motor (MongoDB), PyJWT, Stripe |
| **Frontend** | React 18, Tailwind CSS, Radix UI, Axios |
| **Database** | MongoDB |
| **Email** | Gmail SMTP |
| **Testing** | Pytest, React Testing Library |

## 🎨 Özellik Detayları

### 🏨 15 Hazır Otel
Her biri farklı şehirde (İstanbul, Ankara, İzmir, Antalya, Bursa...)
- Detaylı açıklamalar
- Gerçek fotoğraflar (local)
- Facilities & amenities
- Rating & reviews

### 🏢 60+ Konferans Salonu
- Executive Boardrooms (5-30 kişi)
- Medium Conference Rooms (50-100 kişi)
- Large Event Halls (200-500 kişi)
- Theater-Style Auditoriums (500+ kişi)

### 📧 E-posta Sistemi
- Rezervasyon onay e-postaları (HTML)
- Hoş geldin e-postaları
- Admin bildirimleri
- Professional templates

### 💳 Stripe Ödeme
- Test mode hazır
- Güvenli ödeme akışı
- Webhook desteği
- Success/Cancel pages

### 📊 Dashboard Analytics
- Gelir istatistikleri
- Rezervasyon takibi
- Otel performansı
- Son 10 rezervasyon

### 🔍 SEO
- Meta tags (Open Graph, Twitter)
- Schema.org structured data
- Dynamic sitemap
- robots.txt

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```

**Test Coverage:**
- Authentication tests
- Hotel & Room API tests
- Email service tests

## 📦 Fotoğraf Yönetimi

### Dahil Edilen Fotoğraflar
- **15 Otel:** `/frontend/public/images/hotels/hotel-{1-15}.jpg`
- **20 Salon:** `/frontend/public/images/rooms/room-{1-20}.jpg`
- **Toplam Boyut:** ~3.5 MB

### Yeni Fotoğraf Ekleme
1. Fotoğrafı `/frontend/public/images/` altına koyun
2. Database'de ilgili kayıtta `images` array'ini güncelleyin
3. Veya admin panelinden upload edin

## 🚀 Production Deployment

### Checklist
- [ ] `.env` dosyalarını production değerleriyle güncelleyin
- [ ] Gmail SMTP credentials (production email)
- [ ] Stripe Live API key
- [ ] MongoDB production URL
- [ ] JWT secret key değiştirin
- [ ] Domain'i bağlayın
- [ ] SSL sertifikası ekleyin
- [ ] CORS origins güncelleyin

## 🆘 Troubleshooting

**E-postalar gönderilmiyor:**
- Gmail App Password doğru mu?
- SMTP port 587 açık mı?
- `backend/.env` dosyası doğru yüklendi mi?

**Fotoğraflar görünmüyor:**
- Database seed çalıştırıldı mı?
- `/frontend/public/images/` klasörü var mı?
- Browser cache temizlendi mi?

**MongoDB bağlanamıyor:**
- MongoDB service çalışıyor mu? (`mongod`)
- Port 27017 kullanımda mı?

## 📝 Lisans

MIT License

## 👨‍💻 İletişim

Geliştirici: MeetDelux Team  
Email: info@meetdelux.com

---

**🎯 Not:** Bu repo **self-contained** ve **production-ready**. Clone edip çalıştırmanız yeterli!

**🗑️ Örnek Otelleri Silme:** Admin panel → Hotels → Delete butonu
