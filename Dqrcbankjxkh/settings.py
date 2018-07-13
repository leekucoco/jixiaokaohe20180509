"""
Django settings for MxShop project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os,sys,datetime,djcelery
from celery.schedules import crontab
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z(v$@^23_!%jd$(#z2a-uv)#^iz)u+-bzgtzbx#uxmx+zhn7zs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'corsheaders',
    'rest_framework.authtoken',
    'crispy_forms',
    'django_filters',
    'xadmin',
    'rest_framework',
    'users.apps.UsersConfig',
    'user_operation.apps.UserOperationConfig',
    'depart.apps.DepartConfig',
    'coefficient.apps.CoefficientConfig',
    'certificates.apps.CertificatesConfig',
    'rank13.apps.Rank13Config',
    'salary.apps.SalaryConfig',
    'evaluate.apps.EvaluateConfig',
    'performance.apps.PerformanceConfig',
    'djcelery',
    #'gunicorn',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'Dqrcbankjxkh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Dqrcbankjxkh.wsgi.application'

#DEFAULT_CHARSET = 'utf-8'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "jxkh",
        'USER': 'root',
        'PASSWORD': "leeku853318",
        'HOST': "localhost",
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;SET sql_mode=STRICT_TRANS_TABLES' }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

#设置时区
LANGUAGE_CODE = 'zh-hans'  #中文支持，django1.8以后支持；1.8以前是zh-cn
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False   #默认是Ture，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！！

AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
    #"django.contrib.auth.backends.ModelBackend",
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'WeAdmin/static/')

MEDIA_URL = "/media/"


MEDIA_ROOT = os.path.join(BASE_DIR, "media")



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '30/minute'
    },
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
}



JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.jwt_response_payload_handl.jwt_response_payload_handler'
}

#手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


#云片网设置
APIKEY = '704cb5785af88430dc0267e42184108c'
TPLID = 2341326


#支付宝相关配置
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048.txt')


REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 15
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}




#from djcelery.schedulers import DatabaseScheduler
djcelery.setup_loader()
#BROKER_URL= 'amqp://guest@localhost//'
BROKER_URL= 'redis://localhost:6379/0'

#CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYD_MAX_TASKS_PER_CHILD = 3
BROKER_POOL_LIMIT = 0
#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'  #配置backend
CELERY_TIMEZONE = TIME_ZONE
#CELERYBEAT_SCHEDULER = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#CELERYBEAT_SCHEDULER = 'amqp://guest@localhost//'
# 下面是定时任务的设置，我一共配置了三个定时任务.

CELERYBEAT_SCHEDULE = {
    #定时任务一：　每24小时周期执行任务(del_redis_data)
    u'更新用户等级系数': {
        "task": "coefficient.task.ensurerankleveltask",
        "schedule": crontab(minute=0,hour='*/20'),
        # "schedule": crontab(minute='*/2'),
        "args": (),
    },
    #定时任务二:　每天的凌晨12:30分，执行任务(back_up1)
    u'更新用户投票结果': {
        'task': 'evaluate.task.refreshevaluateresult',
        "schedule": crontab(minute='*/59'),
        #'schedule': crontab(minute=1, hour=0),
        "args": ()
    },
    u'更新未封账工资明细': {
        "task": "salary.task.updatesrecord",
        # "schedule": crontab(minute=0, hour='*/1'),
        "schedule": crontab(minute='*/15'),
        "args": (),
    },

    # #定时任务三:每个月的１号的6:00启动，执行任务(back_up2)
    # u'生成统计报表': {
    #         'task': 'app.tasks.back_up2',
    #         'schedule': crontab(hour=6, minute=0,   day_of_month='1'),
    #         "args": ()
    # },
}
