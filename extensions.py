#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_login import LoginManager
from flask_wtf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy

csrf = CsrfProtect()
login_manager = LoginManager()
db = SQLAlchemy()