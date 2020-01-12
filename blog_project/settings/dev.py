from .base import *
import os
DEBUG= True
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['127.0.0.1']


#Database at development stage
db_password = os.environ.get('DB_PASS')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog2',
        'USER': 'postgres',
        #'PASSWORD': 'rex98756030',
        'PASSWORD': db_password,
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL='post_list'
