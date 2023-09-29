from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_cors import CORS
import os

SECRET_KEY = config('SECRET_KEY')
FLASK_ENV = config('FLASK_ENV')

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b7yg6313a3fkrrhl:hrwtway2sa03k18a@uzb4o9e2oe257glt.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/vsl7sgj741ptkwil'
app.secret_key = SECRET_KEY

CORS(app)

db = SQLAlchemy(app)

# Define tu modelo de datos (por ejemplo, para un blog)
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(255))

# Ruta para una página de bienvenida
@app.route('/welcome', methods=['GET'])
def welcome():
    return "¡Hola! Tu Api Blog funciona."

# Ruta para obtener todas las entradas
@app.route('/getblogs', methods=['GET'])
def get_blogs():
    blogs = BlogPost.query.all()
    return jsonify([{
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image": blog.image
    } for blog in blogs])

# Ruta para obtener una entrada por su ID
@app.route('/getblogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog = BlogPost.query.get(blog_id)
    if blog is None:
        return jsonify({'message': 'Blog no encontrado'}), 404
    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image": blog.image
    })

# Ruta para crear una nueva entrada
@app.route('/create_blog', methods=['POST'])
def create_blog():
    data = request.form
    title = data['title']
    content = data['content']
    image = request.files['image'] if 'image' in request.files else None
    
    # Guardar la imagen si se proporciona
    if image:
        image.save(os.path.join('static/images', image.filename))
        image_path = f'static/images/{image.filename}'
    else:
        image_path = None

    new_blog = BlogPost(title=title, content=content, image=image_path)
    db.session.add(new_blog)
    db.session.commit()

    return jsonify({
        "id": new_blog.id,
        "title": new_blog.title,
        "content": new_blog.content,
        "image": new_blog.image
    }), 201

# Ruta para actualizar una entrada por su ID
@app.route('/update_blog/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = BlogPost.query.get(blog_id)
    if blog is None:
        return jsonify({'message': 'Blog no encontrado'}), 404

    data = request.form
    blog.title = data['title']
    blog.content = data['content']
    
    # Actualizar la imagen si se proporciona una URL
    if 'image' in data:
        blog.image = data['image']

    db.session.commit()

    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image": blog.image
    }), 200

# Ruta para borrar una entrada por su ID
@app.route('/delete_blog/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = BlogPost.query.get(blog_id)
    if blog is None:
        return jsonify({'message': 'Blog no encontrado'}), 404

    db.session.delete(blog)
    db.session.commit()

    return jsonify({'message': 'Blog borrado correctamente'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
