from pathlib import Path
from environs import Env
from datetime import timedelta

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'user.UserAccount'

# Application definition

INSTALLED_APPS = [
    # Theme Package
    'jazzmin',
    # Django App
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party App
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'notifications',
    # Local App
    'user.apps.UserConfig',
    'colleges.apps.CollegesConfig',
    'exams.apps.ExamsConfig',
    'students.apps.StudentsConfig',
    'settings.apps.SettingsConfig',
    'notification.apps.NotificationConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# SIMPLE_JWT = {
#     'AUTH_HEADER_TYPES': ('JWT',),
#     "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
# }
#----------------------------------------------------------------------
JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
}

#----------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Artech API',
    'DESCRIPTION': 'Automatic assessment of artistic colleges aptitude test using deep learning',
    'VERSION': '1.7.23',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # OTHER SETTINGS
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': env.dj_db_url('DATABASE_URL', default='sqlite:///db.sqlite3'),
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT= BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

########################################################################
########################################################################
DJOSER = {
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user_create': ['rest_framework.permissions.AllowAny'],
    },
    # 'SEND_ACTIVATION_EMAIL': True,
    # 'ACTIVATION_URL': 'activate/{uid}/{token}',
    # 'SEND_CONFIRMATION_EMAIL': True,
    # 'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    # 'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    # 'SET_PASSWORD_RETYPE': True,
    # 'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    # 'PASSWORD_RESET_CONFIRM_RETYPE': True,
    # 'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'LOGIN_FIELD': 'email',
    'USER_ID_FIELD': 'id',
    # 'AUTH_TOKEN_CONFIRMATION_EXPIRATION': None,
    # 'PASSWORD_RESET_CONFIRM_TOKEN_EXPIRATION': None,
    # 'USERNAME_RESET_CONFIRM_TOKEN_EXPIRATION': None,
    # 'ACTIVATION_TOKEN_EXPIRATION': None,
    # 'SEND_CONFIRMATION_SET_PASSWORD_EMAIL': True,
    # 'SET_USERNAME_RETYPE': True,
    # 'SET_EMAIL_RETYPE': True,
    # 'TOKEN_MODEL': None,
    # 'LOGIN_AFTER_ACTIVATION': True,
    # 'LOGIN_AFTER_REGISTRATION': True,
    # 'TOKEN_AUTH_HEADER_PREFIX': 'Bearer',
    'TOKEN_AUTH_COOKIE': False,
    'TOKEN_CREATE_REFRESH': False,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'TOKEN_STRATEGY': 'djoser.token.jwt.Token',
    'USERNAME_RESET_CONFIRM_RETYPE': True,
    'SET_USERNAME_RETYPE': True,
    'SET_EMAIL_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'LOGOUT_ON_PASSWORD_CHANGE': False,
    'SERIALIZERS': {
        'current_user': 'user.serializers.UserSerializer',
        'user': 'user.serializers.UserCreateSerializer',
        'user_create': 'user.serializers.UserCreateSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
        'user_list': 'djoser.serializers.UserSerializer',
        'user_password': 'djoser.serializers.UserPasswordSerializer',
        'user_reset_password': 'djoser.serializers.UserPasswordResetSerializer',
        'username_reset': 'djoser.serializers.UsernameResetSerializer',
        'password_reset': 'djoser.serializers.PasswordResetSerializer',
        'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
        'set_password': 'djoser.serializers.SetPasswordSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
        'token_refresh': 'djoser.serializers.TokenRefreshSerializer',
        'token_verify': 'djoser.serializers.TokenVerifySerializer',
        }
    }
########################################################################
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title":
    "Artech Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header":
    "Artech",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand":
    "Artech",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo":
    "icons/icon.ico",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo":
    "icons/icon.ico",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark":
    "icons/icon.ico",

    # CSS classes that are applied to the logo above
    "site_logo_classes":
    "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon":
    "icons/icon.ico",

    # Welcome text on the login screen
    "welcome_sign":
    "Welcome to the Artech Admin Panel",

    # Copyright on the footer
    "copyright":
    "Fares Emad (Scorpion)",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": ["auth.User", "auth.Group"],

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"]
        },

        # external url that opens in a new window (Permissions can be added)
        {
            "name": "GitHub",
            "url": "https://github.com/faresemad",
            "new_window": True
        },

        # model admin to link to (Permissions checked against model)
        {
            "model": "users.student"
        },

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {
            "app": "users",
        },
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {
            "name": "GitHib",
            "url": "https://github.com/faresemad",
            "new_window": True
        },
        {
            "name": "Facebook",
            "url": "https://www.facebook.com/faresemadx",
            "new_window": True
        },
        {
            "name": "Instagram",
            "url": "https://www.instagram.com/faresemadx",
            "new_window": True
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/in/faresemad/",
            "new_window": True
        },
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar":
    True,

    # Whether to aut expand the menu
    "navigation_expanded":
    True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents":
    "fas fa-chevron-circle-right",
    "default_icon_children":
    "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active":
    False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css":
    "css/main.css",
    "custom_js":
    None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn":
    True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder":
    True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format":
    "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs"
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-gray navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
