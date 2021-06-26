import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7)c*jo@@)a^3m08b-+54d3d2nx(=3k^es!5z&=v*0zt(%z3mmf'#後でherokuに使う

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
