from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_cors import CORS
import jwt
import os

#A secret key is established for JWT (JSON Web Tokens)
SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'claverandom'
SECRET_KEY = config('SECRET_KEY')
FLASK_ENV = config('FLASK_ENV')

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = SECRET_KEY

#Allow this API to be accessible from a different origin
CORS(app)

db = SQLAlchemy(app)

# Defining a data model (BlogsPost)
#Create a template for blog posts, with an id, title, content, and a path to an image.
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    image = db.Column(db.String(1000))

# Route to a welcome page
@app.route('/welcome', methods=['GET'])
def welcome():
    return "¡Hola! Tu Api Blog funciona."

# Route to get all entries
@app.route('/getblogs', methods=['GET'])
def get_blogs():
    blogs = BlogPost.query.all()
    return jsonify([{
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image": blog.image
    } for blog in blogs])

# Route to get an entry by your ID
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

# Route to create a new entry
@app.route('/create_blog', methods=['POST'])
def create_blog():
    data = request.form
    title = data['title']
    content = data['content']
    image = request.form.get('image')

    print(request.files) 
    
    # Save the image if the user wants
    if image:
        image_path = image
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

# Route to update an entry by its ID
@app.route('/update_blog/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = BlogPost.query.get(blog_id)
    if blog is None:
        return jsonify({'message': 'Blog no encontrado'}), 404

    data = request.form
    blog.title = data['title']
    blog.content = data['content']
    
    # Update image if a URL is provided
    if 'image' in data:
        blog.image = data['image']

    db.session.commit()

    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image": blog.image
    }), 200

# Route to delete an entry by its ID
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
