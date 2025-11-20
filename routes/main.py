from flask import Blueprint, render_template, jsonify
from models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get featured products
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    
    return render_template('index.html', featured_products=featured_products)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/categories')
def categories():
    # Get all products for categories page
    all_products = Product.query.all()
    
    categories_data = {
        'projects': {
            'name': 'Dasturiy Loyihalar',
            'count': Product.query.filter_by(category='projects').count(),
            'icon': 'project-diagram'
        },
        'hardware': {
            'name': 'Kompyuter Texnikasi',
            'count': Product.query.filter_by(category='hardware').count(),
            'icon': 'laptop'
        },
        'components': {
            'name': 'Komponentlar',
            'count': Product.query.filter_by(category='components').count(),
            'icon': 'microchip'
        },
        'accessories': {
            'name': 'Aksessuarlar',
            'count': Product.query.filter_by(category='accessories').count(),
            'icon': 'keyboard'
        }
    }
    
    return render_template('categories.html', 
                         categories=categories_data, 
                         all_products=all_products)