from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Product, Cart, Review

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def user_profile():
    # Foydalanuvchi ma'lumotlari
    user_products = Product.query.filter_by(seller_id=current_user.id).order_by(Product.created_at.desc()).all()
    user_reviews = Review.query.filter_by(author_id=current_user.id).order_by(Review.created_at.desc()).all()
    
    return render_template('profile/profile.html', 
                         user_products=user_products,
                         user_reviews=user_reviews)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
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

@profile_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
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
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Savatcha tozalandi', 'success')
    return redirect(url_for('profile.cart'))

@profile_bp.route('/favorites')
@login_required
def favorites():
    # Favorite modeli yo'qligi sababli, Cart dan foydalanamiz (quantity=0 bo'lsa favorite deb hisoblaymiz)
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