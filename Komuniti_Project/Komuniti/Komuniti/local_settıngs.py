SECRET_KEY = '-^%osj2asg*)+bd7654erfgdjs$ucqx5p=&fj)l630&o96hqmhy#l*-ps_&(3q'

DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'komuniti2',
        'USER': 'kommy',
        'PASSWORD': '12345',
        'HOST':'localhost',
        'PORT':'5432'

    }
}