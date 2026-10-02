# caravaning_project/settings.py

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# Configuración privada de seguridad
SECRET_KEY_FILE = Path.home() / ".caravaning_secret"

SECRET_KEY = SECRET_KEY_FILE.read_text().strip().split("=", 1)[1]

SECRET_KEY_FALLBACKS = []


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'caravaning.pythonanywhere.com',
    'caravaning-project.online',
    'www.caravaning-project.online',
    'localhost',
    '127.0.0.1',
]

# Amazon Afiliados
AMAZON_ASSOCIATE_TAG = 'caravaning0b-21'
AMAZON_MARKETPLACE_HOSTS = ('amazon.es', 'www.amazon.es')


# Application definition

INSTALLED_APPS = [
    'community',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # Mis aplicaciones
    'destinations.apps.DestinationsConfig',
    'users.apps.UsersConfig',
    'listings.apps.ListingsConfig',
    'blog.apps.BlogConfig',
    'shop.apps.ShopConfig',
    'pages.apps.PagesConfig',
    'ferries.apps.FerriesConfig',
    'experiences.apps.ExperiencesConfig',
    'messaging.apps.MessagingConfig',
    'widget_tweaks',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'caravaning.middleware.HTMLNoStoreMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'caravaning.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'caravaning.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Directorios donde Django buscará archivos estáticos adicionales,
# además de las carpetas 'static' de cada aplicación.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Directorio donde se copiarán todos los archivos estáticos para producción.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de archivos de medios (imágenes subidas por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de Email (para desarrollo)
# Los emails se imprimirán en la consola en lugar de ser enviados.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@caravaning.com'

# Redirecciones de autenticación
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'users:login'

# Configuración de CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source', 'Table'],
            ['Format', 'FontSize', 'TextColor', 'BGColor'],
        ],
        'width': '100%',
        'removePlugins': 'exportpdf',
    },
}
ALOHACAMP_AFFILIATE_URL = "https://r.alohacamp.com/caravaning"

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


# Correo electrónico de Caravaning Project
import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "creacionesms@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

if not EMAIL_HOST_PASSWORD:
    _gmail_file = (
        Path.home()
        / ".config"
        / "caravaning"
        / "gmail_password"
    )

    if _gmail_file.is_file():
        EMAIL_HOST_PASSWORD = (
            _gmail_file.read_text(encoding="utf-8").strip()
        )

DEFAULT_FROM_EMAIL = (
    "Caravaning Project <creacionesms@gmail.com>"
)

EMAIL_TIMEOUT = 15


# HTTPS: HSTS inicial de cinco minutos
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
