INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites', 

    'django_extensions',
    'clear_cache',


    #3rd party apps

    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth', 
    'allauth.account', 
    'allauth.socialaccount',
    'rest_auth.registration', 
    'drf_yasg',
    'corsheaders',
    'django_filters',
    #internal apps
    'project.apps.catalogue',
    'project.apps.order',

)

AUTH_USER_MODEL = 'User.Users'
SITE_ID = 1 