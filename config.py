#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import timedelta


class Config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILES_DIR = os.path.join(BASE_DIR, 'files')
    UPLOAD_DIR = os.path.join(FILES_DIR, 'uploads')
    DOWNLOAD_DIR = os.path.join(FILES_DIR, 'downloads')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    REMEMBER_COOKIE_DURATION = timedelta(seconds=3600 * 8)  # set session timeout time
    WTF_CSRF_CHECK_DEFAULT = False
    SECRET_KEY = os.urandom(32)


class Dev(Config):
    DEBUG = True
    DATABASE = {
        'host': 'localhost',
        'port': 3306,
        'user': 'docker',
        'passwd': 'docker',
        'db': 'zzz'
    }
    # Flask-Sqlalchemy 配置
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passwd}@{host}:{port}/{db}'.format(**DATABASE)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CAS_TOKEN_VALIDATE_URL = 'http://192.168.90.74:8080/cas/p3/serviceValidate'
    CAS_LOGIN_URL = 'https://192.168.90.74:8443/cas/login'
    CAS_LOGOUT_URL = 'https://192.168.90.74:8443/cas/logout'

class Prod(Config):
    pass