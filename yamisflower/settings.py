"""
Django settings for yamisflower project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

############################################################
# MySQL 세팅
from pymysql import install_as_MySQLdb
install_as_MySQLdb()

def mysqldb_escape(value, conv_dict):
    from pymysql.converters import encoders
    vtype = type(value)
    # note: you could provide a default:
    # PY2: encoder = encoders.get(vtype, escape_str)
    # PY3: encoder = encoders.get(vtype, escape_unicode)
    encoder = encoders.get(vtype)
    return encoder(value)

import pymysql
setattr(pymysql, 'escape', mysqldb_escape)
del pymysql
############################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7xx6ca2xcmd@bh+p_t@ojr_cn@ffm30mg!d*bxgvl!p*s^npz@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Only allow host to contadr.org
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'bootstrap3',
    'imagekit',
    'django_extensions',
    'debug_toolbar',
    'el_pagination',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',

    'shop',
    'accounts',
    
    'django_cleanup',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yamisflower.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'yamisflower', 'templates')
        ],
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

WSGI_APPLICATION = 'yamisflower.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_yamisflower', # DB명
        'USER': 'root', # 데이터베이스 계정
        'PASSWORD': '11111111', # 계정 비밀번호
        'HOST': 'localhost', # 데이테베이스 주소(IP)
        'PORT': '3306', # 데이터베이스 포트(보통은 3306)
    }
}

DATE_INPUT_FORMATS = ('%d-%m-%Y')


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # 장고 기본 인증 시스템
    'allauth.account.auth_backends.AuthenticationBackend', # 추가
]

SITE_ID = 1 # 이걸 1로 해야 하나의 site 참조

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none' # 이메일 인증 x


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'yamisflower', 'static'),
] # static 기본 디렉터리 경로를 yamisflower/static으로 한다.
# 배포할 때에 합칠 디렉터리 지정
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# messages
from django.contrib.messages import constants

MESSAGE_LEVEL = constants.DEBUG # debug 레벨의 messages 사용 가능

# django messages에서의 error 처리를 하지만 bootstrap에는 error 라는 클래스가 없다.
# 이를 위해 error 메세지 태그를 danger로 바꾸어 화면에 뿌려준다.
MESSAGE_TAGS = {constants.ERROR:'danger'}

CORS_ORIGIN_ALLOW_ALL = True

# debug_toolbar를 제공할 ip (개발자 ip)
INTERNAL_IPS = ['255.255.255.255']