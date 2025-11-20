from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Product, Review, Cart
from forms import ProductForm, ReviewForm

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def product_list():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = Product.query
    
    if category != 'all':
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.title.ilike(f'%{search}%'))
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('products/list.html', 
                         products=products, 
                         category=category,
                         search=search)

@products_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    
    return render_template('products/detail.html', product=product, form=form)

@products_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm(request.form) if request.method == 'POST' else ProductForm()
    
    if request.method == 'POST' and form.validate():
        product = Product(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            condition=form.condition.data,
            image_url=form.image_url.data or '/static/images/default-product.png',
            seller_id=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Mahsulot muvaffaqiyatli qo\'shildi!', 'success')
        return redirect(url_for('products.product_detail', product_id=product.id))
    
    return render_template('products/create.html', form=form)

@products_bp.route('/products/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    form = ReviewForm(request.form)
    product = Product.query.get_or_404(product_id)
    
    if form.validate():
        review = Review(
            content=form.content.data,
            rating=form.rating.data,
            author_id=current_user.id,
            product_id=product_id
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Sharhingiz qo\'shildi!', 'success')
    
    return redirect(url_for('products.product_detail', product_id=product_id))

@products_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    existing_item = Cart.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.title} savatchaga qo\'shildi', 'success')
    
    return redirect(request.referrer or url_for('main.index'))

@products_bp.route('/api/products')
def api_products():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = Product.query
    
    if category != 'all':
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.title.ilike(f'%{search}%'))
    
    products = query.order_by(Product.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'price': p.price,
        'category': p.category,
        'condition': p.condition,
        'seller': p.seller.username,
        'image_url': p.image_url,
        'created_at': p.created_at.isoformat()
    } for p in products])