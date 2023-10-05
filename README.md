# API de Blog

This is an API for managing blog posts using Flask and MySQL.

## API URL

https://cactus-api-blog2-c3df13e82454.herokuapp.com

### Instalación

Install the dependencies using pip: pip install -r requirements.txt

## Use

Run the application using the following command: python app.py
The API will be available at `http://localhost:5000`.

## Routes

`GET /welcome`: Welcome page
- `GET /getblogs`: Gets all blog posts.
- `GET /getblogs/<int:blog_id>`: Gets a specific entry by its ID.
- `POST /create_blog`: Create a new blog post.
- `PUT /update_blog/<int:blog_id>`: Updates an existing entry by its ID.
- `DELETE /delete_blog/<int:blog_id>`: Delete an existing entry by its ID.





