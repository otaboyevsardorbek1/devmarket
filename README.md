# DevMarket - Dasturchilar uchun bozor platformasi

![DevMarket Logo](static/images/logo.png)

## Loyiha haqida

DevMarket - bu dasturchilar va IT mutaxassislari uchun mo'ljallangan maxsus bozor platformasi. Loyiha Flask framework'i asosida ishlab chiqilgan.

## Xususiyatlar

### 🛍️ Asosiy funksiyalar
- **Mahsulotlar katalogi** - turli xil dasturiy mahsulotlar va xizmatlar
- **Kategoriyalar** - mahsulotlarni turli toifalarga bo'lish
- **Qidiruv tizimi** - tez va samarali qidiruv
- **Foydalanuvchi profillari** - sotuvchilar va xaridorlar uchun profil tizimi

### 🔐 Xavfsizlik
- **Foydalanuvchi autentifikatsiyasi** - xavfsiz ro'yxatdan o'tish va kirish
- **Ma'lumotlarni himoyalash** - shaxsiy ma'lumotlarning xavfsizligi
- **Xavfsiz to'lov tizimi** - ishonchli to'lov operatsiyalari

### 💼 Sotuvchilar uchun
- **Mahsulot qo'shish** - oson mahsulot joylashtirish
- **Buyurtmalarni boshqarish** - buyurtmalarni kuzatish
- **Statistika** - sotuvlar statistikasi

## O'rnatish va ishga tushirish

### Talablar
- Python 3.8+
- Flask
- SQLAlchemy
- Virtual environment

### O'rnatish bosqichlari

1. **Loyihani yuklab olish**:
git clone [repository-url]
cd devmarket
Virtual muhit yaratish:

python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
Kutubxonalarni o'rnatish:

pip install -r requirements.txt
Ma'lumotlar bazasini sozlash:

python init_db.py
Dasturni ishga tushirish:

python app.py
Dastur http://localhost:5000 manzilida ishga tushadi.

Loyiha strukturasi
text
devmarket/
├── app.py                 # Asosiy Flask aplikatsiya
├── config.py             # Sozlamalar
├── models.py             # Ma'lumotlar bazasi modellari
├── init_db.py            # Ma'lumotlar bazasini ishga tushirish
├── requirements.txt      # Python kutubxonalari
├── static/              # Statik fayllar
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML shablonlar
    ├── base.html
    ├── index.html
    ├── partials/
    └── ...
Foydalanish
Foydalanuvchi sifatida:
Ro'yxatdan o'ting yoki tizimga kiring

Mahsulotlarni ko'rib chiqing

Qidiruv orqali kerakli mahsulotni toping

Savatga qo'shing va buyurtma bering

Sotuvchi sifatida:
Profilingizni to'ldiring

Yangi mahsulot qo'shing

Buyurtmalarni boshqaring

Statistikalarni ko'ring

Ishlab chiqish
Yangi funksiya qo'shish:
Yangi branch yarating

O'zgartirishlarni amalga oshiring

Testlarni yozing

Pull request yuboring

Testlash:
bash
python -m pytest tests/
Yordam
Agar sizda savollar bo'lsa:

GitHub Issues bo'limida yangi issue oching

Email orqali bog'laning: [email manzilingiz]

Telegram: [telegram username]

Litsenziya
Bu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun LICENSE faylini ko'ring.

Hamkorlik
Loyihani takomillashtirishga hissa qo'shmoqchi bo'lgan har bir dasturchi pull requestlar orqali qo'shisha oladi.

Yangilanishlar
v1.0.0 - Loyihaning birinchi versiyasi

Asosiy funksiyalar ishga tushirildi

Ma'lumotlar bazasi strukturasi yaratildi

Foydalanuvchi interfeysi ishlab chiqildi

Ishlab chiqilgan vaqti: 2025-yil

Ishlab chiqaruvchi: [Ismingiz]

text

Ushbu matnni nusxalab oling va GitHub repositorysiga `README.md` nomi bilan yuklang. Agar sizda repository URL manzili yoki boshqa o'zgartirishlar kerak bo'lsa, men yordam beraman!
