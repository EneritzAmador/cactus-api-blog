from decouple import config

SECRET_KEY = config('SECRET_KEY')
FLASK_ENV = config('FLASK_ENV', default='development')