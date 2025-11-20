from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Database initialization
    db.init_app(app)
    
    # Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Iltimos, tizimga kiring'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Blueprint registrations
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.main import main_bp
    from routes.profile import profile_bp  # Yangi qo'shildi
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)  # Yangi qo'shildi
    
    # Error handlers
    from datetime import datetime
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html', now=datetime.now()), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html', now=datetime.now()), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html', now=datetime.now()), 403
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('400.html', now=datetime.now()), 400
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        # Seed initial data
        try:
            from utils.seed import seed_data
            seed_data()
            print("Ma'lumotlar bazasi muvaffaqiyatli to'ldirildi!")
        except Exception as e:
            print(f"Seed ma'lumotlarini yuklashda xatolik: {e}")
    
    app.run(debug=True)