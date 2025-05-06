import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Instancia Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Importar modelos
from app.models import Post, Category

# Importar y registrar Blueprints
from app.routes.post import posts_bp
app.register_blueprint(posts_bp, url_prefix='/posts')

from app.routes.category import categories_bp
app.register_blueprint(categories_bp, url_prefix='/categories')


# Crear tablas
with app.app_context():
    db.create_all()

# Ruta principal
@app.route('/')
def index():
    return redirect(url_for('posts.listar_posts'))

if __name__ == '__main__':
    app.run(debug=True)

