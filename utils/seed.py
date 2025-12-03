import json
from models import db, User, Product, Review
from werkzeug.security import generate_password_hash

def seed_data():
    # Check if data already exists
    if User.query.first() is not None:
        print("Ma'lumotlar bazasi allaqachon to'ldirilgan")
        return
    
    # Create sample users
    users = [
        User(
            username='Azizbek',
            email='azizbek@example.com',
            password_hash=generate_password_hash('password123')
        ),
        User(
            username='DasturTexnika',
            email='texnika@example.com',
            password_hash=generate_password_hash('password123')
        ),
        User(
            username='PythonDev',
            email='python@example.com',
            password_hash=generate_password_hash('password123')
        )
    ]
    
    for user in users:
        db.session.add(user)
    #devmarket\static\images\demo\soft_market_logo.jpg
    db.session.commit()
    Default_praducts_img ='https://devmarket.in/logo.png'
    # Create sample products
    products = [
        Product(
            title="E-ticaret veb-sayti",
            description="React va Node.js asosida yaratilgan to'liq funksional elektron tijorat veb-sayti. Admin paneli, to'lov tizimi va mobil moslashuvli dizayn.",
            price=500.00,
            category="projects",
            condition="new",
            image_url=Default_praducts_img,
            seller_id=1
        ),
        Product(
            title="MacBook Pro M1",
            description="2022 yilgi MacBook Pro M1 protsessori, 16GB RAM, 512GB SSD. Ideal dasturlash uchun. Holati a'lo.",
            price=1200.00,
            category="hardware",
            condition="used",
            image_url=Default_praducts_img,
            seller_id=2
        ),
        Product(
            title="RTX 3080 Videokarta",
            description="NVIDIA GeForce RTX 3080 10GB. O'yin va grafik dasturlash uchun a'lo. 6 oy ishlatilgan, kafolati bor.",
            price=700.00,
            category="components",
            condition="used",
            image_url=Default_praducts_img,
            seller_id=2
        ),
        Product(
            title="Mobil Ilova UI Kit",
            description="Figma uchun tayyor UI komponentlari to'plami. React Native va Flutter loyihalari uchun moslashtirilgan.",
            price=150.00,
            category="projects",
            condition="new",
            image_url=Default_praducts_img,
            seller_id=3
        )
    ]
#
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    
    # Create sample reviews
    reviews = [
        Review(
            content="A'lo mahsulot! Dastur juda yaxshi ishlaydi va kod sifatli.",
            rating=5,
            author_id=2,
            product_id=1
        ),
        Review(
            content="Yaxshi loyiha, lekin hujjatlarni yaxshiroq tuzish kerak.",
            rating=4,
            author_id=3,
            product_id=1
        )
    ]
    
    for review in reviews:
        db.session.add(review)
    
    db.session.commit()
    
    print("Ma'lumotlar bazasi muvaffaqiyatli to'ldirildi!")