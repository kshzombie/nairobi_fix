import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-r@7(wk#@o=xy^u==v8!#0c43wzxrg6c2hcqcl_gs(yartl)1_x'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis', # Essential for PostGIS
    'reports.apps.ReportsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- LOCAL DATABASE (PostgreSQL/PostGIS) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres', # Change this if you created a specific DB like 'urban_fix_db'
        'USER': 'postgres',
        'PASSWORD': 'Proffess1onal@SQL',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# --- WINDOWS GIS CONFIGURATION (Conda) ---
# This section tells Django exactly where your Miniconda GIS libraries are.
if os.name == 'nt':
    # Path to your Miniconda environment
    CONDA_ENV_PATH = r"C:\Users\oduor\miniconda3\envs\webgis_env"
    
    # Pointing to the GDAL DLL
    GDAL_LIBRARY_PATH = os.path.join(CONDA_ENV_PATH, 'Library', 'bin', 'gdal.dll')
    
    # Setting the PROJ data directory (required for coordinate transformations)
    os.environ['PROJ_LIB'] = os.path.join(CONDA_ENV_PATH, 'Library', 'share', 'proj')
    
    # Adding the bin folder to the system path so Django can see GEOS and other DLLs
    os.environ['PATH'] = os.path.join(CONDA_ENV_PATH, 'Library', 'bin') + os.pathsep + os.environ['PATH']


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'