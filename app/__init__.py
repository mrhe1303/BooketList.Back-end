import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.database import db, migrate

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave-por-defecto")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///biblioteca.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "clave-jwt-secreta")
    
    print(f"🔑 SECRET_KEY cargada: {'✅' if app.config['SECRET_KEY'] else '❌'}")
    print(f"🗄️ DATABASE_URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # ✅ CONFIGURACIÓN CORS CORREGIDA
    CORS(app, 
         resources={
             r"/api/*": {
                 "origins": [
                     "http://localhost:5173", 
                     "http://127.0.0.1:5173",
                     "http://localhost:3000",
                     "http://127.0.0.1:3000"
                 ],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True
             }
         })
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    
    # Importar y registrar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # Registrar manejadores de errores
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    with app.app_context():
        db.create_all()
    
    return app