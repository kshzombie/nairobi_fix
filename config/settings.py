import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# --- ENVIRONMENT DETECTION ---
ON_PYTHONANYWHERE = 'PYTHONANYWHERE_DOMAIN' in os.environ

SECRET_KEY = 'django-insecure-r@7(wk#@o=xy^u==v8!#0c43wzxrg6c2hcqcl_gs(yartl)1_x'

if ON_PYTHONANYWHERE:
    DEBUG = False
    ALLOWED_HOSTS = ['kshzombie.pythonanywhere.com']
else:
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
    'django.contrib.gis',
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

# --- DATABASE & GIS CONFIGURATION ---
if ON_PYTHONANYWHERE:
    # PythonAnywhere Production Settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    # These paths were verified via your 'ls' command
    GDAL_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/libgdal.so.34'
    GEOS_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/libgeos_c.so.1'
    SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
else:
    # Local Development Settings (Windows/PostGIS)
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'urban_fix_db',
            'USER': 'postgres',
            'PASSWORD': 'Proffess1onal@SQL',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    # Local Windows Conda GDAL Configuration
    if os.name == 'nt':
        CONDA_ENV_PATH = r"C:\Users\oduor\miniconda3\envs\webgis_env"
        GDAL_LIBRARY_PATH = os.path.join(CONDA_ENV_PATH, 'Library', 'bin', 'gdal.dll')
        os.environ['PROJ_LIB'] = os.path.join(CONDA_ENV_PATH, 'Library', 'share', 'proj')
        os.environ['PATH'] = os.path.join(CONDA_ENV_PATH, 'Library', 'bin') + os.pathsep + os.environ['PATH']

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'