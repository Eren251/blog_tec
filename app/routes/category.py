from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/')
def listar_categorias():
    categories = Category.query.all()
    return render_template('categories/listar_categorias.html', categories=categories)

@categories_bp.route('/new', methods=['GET', 'POST'])
def add_categoria():
    if request.method == 'POST':
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('categories.listar_categorias'))
    return render_template('categories/create_categoria.html')

@categories_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def update_categoria(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']
        db.session.commit()
        return redirect(url_for('categories.listar_categorias'))
    return render_template('categories/edit_categoria.html', category=category)

@categories_bp.route('/delete/<int:id>')
def delete_categoria(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.listar_categorias'))
