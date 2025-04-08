import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv 

#Cargar las variables de entorno
load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Importar modelos para que SQLAlchemy los reconozca
from app.models import Post
from app.models import Category

#Importar y registrar blueprints
from app.routes.post import posts_bp

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

app.register_blueprint(posts_bp, url_prefix='/posts')

#Ruta principal home
@app.route('/')
def index():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('index.html', posts=posts, categories=categories)

#Ruta /post crear un nuevo post
@app.route('/posts/new', methods=['GET','POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category_id')
        new_post = Post(title=title, content=content, category_id=category_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))
    
    #Aqui sigue si es GET
    categories = Category.query.all()
    return render_template('create_post.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)