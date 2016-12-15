#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask


def create_app():
    from extensions import csrf
    from extensions import login_manager
    from extensions import db
    from views.main import main
    from views.auth import auth

    app=Flask(__name__)
    env = os.environ.get('zen_env', 'dev')
    app.config.from_object('config.Prod') if env == 'prod' else app.config.from_object('config.Dev')
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(main, url_prefix=None)
    app.register_blueprint(auth, url_prefix='/auth')
    login_manager.login_view = 'auth.login'
    return app
