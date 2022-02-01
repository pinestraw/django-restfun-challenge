import sys
from decouple import config

# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'hidayah',
#         'USER': 'my_user',
#         'PASSWORD': 'p@ssw0rd',
#         'HOST': '127.0.0.1',
#         'CONN_MAX_AGE': 900
#     }
# }

# DATABASES = {
#     'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': config('DB_NAME'),
#             'USER': config('DB_USER'),
#             'PASSWORD': config('DB_PASSWORD'),
#             'HOST': config('DB_HOST'),
#             'PORT': config('DB_PORT'),
#             'CONN_MAX_AGE': 60,
#             'ATOMIC_REQUESTS': True
#         }
# }
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

AUTH_USER_MODEL='auth.User'