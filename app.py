from flask import Flask
from config import Config
from models.movie import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация базы данных
    db.init_app(app)

    # Регистрация маршрутов
    from routes.main_routes import main_bp
    from routes.developer_routes import developer_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(developer_bp, url_prefix='/developer')

    return app


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()
        print("✅ Database tables created")

    print("🚀 Starting Movie Search App...")
    print("📍 http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)