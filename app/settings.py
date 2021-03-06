# -*- coding: utf-8 -*-
import os
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
os_env = os.environ


class Config(object):
    SECRET_KEY = '3nFca3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""
    # app config
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    HOST = '0.0.0.0'
    #TEMPLATES_AUTO_RELOAD = False
    # Celery background task config
    # CELERY_BROKER_URL = 'redis://:1234567a@@27.72.147.222:6379/0'
    # CELERY_BACKEND_URL = 'redis://:1234567a@@27.72.147.222:6379/0'
    # JWT Config
    # JWT_SECRET_KEY = '1234567a@'
    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # SQL Alchemy config
    # MongoDB config
    # MONGO_DBNAME = 'dhpg'
    # MONGO_AUTH_SOURCE = 'admin'
    # MONGO_CONNECT = False
    # CONNECT = False
    # Email setting
    # MAIL_DEFAULT_SENDER = 'DHPG'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = 'demo@gmail.com'
    # MAIL_PASSWORD = 'emailpassword'
    # REDIS
    #REDIS_URL = "redis://:1234567a@@27.72.147.222:6379/0"


class DevConfig(Config):
    """Development configuration."""
    # app config
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    TEMPLATES_AUTO_RELOAD = True
    HOST = '0.0.0.0'
    # Celery background task config
    #CELERY_BROKER_URL = 'redis://localhost:6379/0'
    #CELERY_BACKEND_URL = 'redis://localhost:6379/0'
    # JWT Config
    # JWT_SECRET_KEY = '1234567a@@'
    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # SQL Alchemy config
    # MongoDB config
    # MONGO_DBNAME = 'dhpg'
    # MONGO_HOST = 'localhost'
    # MONGO_CONNECT = False
    # CONNECT = False
    # Email setting
    # Email setting
    # MAIL_DEFAULT_SENDER = 'Project name'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = 'demo@gmail.com'
    # MAIL_PASSWORD = 'emailpassword'
    # REDIS
    # REDIS_URL = "redis://localhost:6379/0"
