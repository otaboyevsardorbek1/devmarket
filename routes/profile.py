from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Product, Cart, Review, Message
import os
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

# Rasm fayllari uchun ruxsat etilgan formatlar
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/profile')
@login_required
def user_profile():
    # Foydalanuvchi ma'lumotlari
    user_products = Product.query.filter_by(seller_id=current_user.id).order_by(Product.created_at.desc()).all()
    user_reviews = Review.query.filter_by(author_id=current_user.id).order_by(Review.created_at.desc()).all()
    
    # Savat va sevimlilar soni
    cart_count = Cart.query.filter_by(user_id=current_user.id).filter(Cart.quantity > 0).count()
    favorites_count = Cart.query.filter_by(user_id=current_user.id, quantity=0).count()
    
    return render_template('profile/profile.html', 
                         user_products=user_products,
                         user_reviews=user_reviews,
                         cart_count=cart_count,
                         favorites_count=favorites_count)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # Profil rasmini yuklash
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file_path = os.path.join(current_app.root_path, 'static', 'uploads', 'profiles', filename)
                
                # Papkani yaratish
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Eski rasmni o'chirish
                if current_user.profile_image and current_user.profile_image != '/static/images/default-avatar.png':
                    old_file_path = os.path.join(current_app.root_path, current_user.profile_image.lstrip('/'))
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Yangi rasmni saqlash
                file.save(file_path)
                current_user.profile_image = f'/static/uploads/profiles/{filename}'
        
        if username and len(username) >= 3:
            current_user.username = username
        
        if email and '@' in email:
            # Email unikalligini tekshirish
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Bu elektron pochta bilan foydalanuvchi mavjud', 'error')
            else:
                current_user.email = email
        
        db.session.commit()
        flash('Profil muvaffaqiyatli yangilandi!', 'success')
        return redirect(url_for('profile.user_profile'))
    
    return render_template('profile/edit_profile.html')

@profile_bp.route('/profile/remove-image', methods=['POST'])
@login_required
def remove_profile_image():
    if current_user.profile_image and current_user.profile_image != '/static/images/default-avatar.png':
        # Faylni o'chirish
        file_path = os.path.join(current_app.root_path, current_user.profile_image.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Default rasmga o'zgartirish
        current_user.profile_image = '/static/images/default-avatar.png'
        db.session.commit()
        flash('Profil rasmi o\'chirildi', 'success')
    
    return redirect(url_for('profile.edit_profile'))

@profile_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).filter(Cart.quantity > 0).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('profile/cart.html', 
                         cart_items=cart_items,
                         total_price=total_price)

@profile_bp.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    
    if cart_item.user_id != current_user.id:
        flash('Ruxsat yo\'q', 'error')
        return redirect(url_for('profile.cart'))
    
    action = request.form.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'remove':
        db.session.delete(cart_item)
        db.session.commit()
        flash('Mahsulot savatchadan olib tashlandi', 'success')
        return redirect(url_for('profile.cart'))
    
    db.session.commit()
    return redirect(url_for('profile.cart'))

@profile_bp.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    Cart.query.filter_by(user_id=current_user.id).filter(Cart.quantity > 0).delete()
    db.session.commit()
    flash('Savatcha tozalandi', 'success')
    return redirect(url_for('profile.cart'))

@profile_bp.route('/favorites')
@login_required
def favorites():
    favorite_items = Cart.query.filter_by(user_id=current_user.id, quantity=0).all()
    
    return render_template('profile/favorites.html', favorite_items=favorite_items)

@profile_bp.route('/favorites/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_favorites(product_id):
    product = Product.query.get_or_404(product_id)
    
    existing_favorite = Cart.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id,
        quantity=0
    ).first()
    
    if not existing_favorite:
        favorite_item = Cart(user_id=current_user.id, product_id=product_id, quantity=0)
        db.session.add(favorite_item)
        db.session.commit()
        flash(f'{product.title} sevimlilarga qo\'shildi', 'success')
    else:
        flash('Bu mahsulot allaqachon sevimlilarda', 'info')
    
    return redirect(request.referrer or url_for('main.index'))

@profile_bp.route('/favorites/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_favorites(cart_id):
    favorite_item = Cart.query.get_or_404(cart_id)
    
    if favorite_item.user_id != current_user.id:
        flash('Ruxsat yo\'q', 'error')
        return redirect(url_for('profile.favorites'))
    
    db.session.delete(favorite_item)
    db.session.commit()
    flash('Mahsulot sevimlilardan olib tashlandi', 'success')
    return redirect(url_for('profile.favorites'))

# Xabar jo'natish funksiyalari
@profile_bp.route('/messages')
@login_required
def messages():
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    
    return render_template('profile/messages.html', 
                         received_messages=received_messages,
                         sent_messages=sent_messages)

@profile_bp.route('/messages/send/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def send_message(receiver_id):
    receiver = User.query.get_or_404(receiver_id)
    product_id = request.args.get('product_id')
    product = Product.query.get(product_id) if product_id else None
    
    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')
        
        if not subject or not content:
            flash('Mavzu va xabar matnini to\'ldiring', 'error')
            return render_template('profile/send_message.html', 
                                 receiver=receiver, 
                                 product=product)
        
        message = Message(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            product_id=product_id,
            subject=subject,
            content=content
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('Xabar muvaffaqiyatli yuborildi', 'success')
        return redirect(url_for('profile.messages'))
    
    return render_template('profile/send_message.html', 
                         receiver=receiver, 
                         product=product)

@profile_bp.route('/messages/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    # Faqat yuboruvchi yoki qabul qiluvchi ko'ra oladi
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        flash('Ruxsat yo\'q', 'error')
        return redirect(url_for('profile.messages'))
    
    # Xabarni o'qilgan deb belgilash
    if message.receiver_id == current_user.id and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('profile/view_message.html', message=message)

@profile_bp.route('/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    # Faqat yuboruvchi yoki qabul qiluvchi o'chira oladi
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        flash('Ruxsat yo\'q', 'error')
        return redirect(url_for('profile.messages'))
    
    db.session.delete(message)
    db.session.commit()
    flash('Xabar o\'chirildi', 'success')
    return redirect(url_for('profile.messages'))