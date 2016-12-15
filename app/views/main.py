#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_login import login_required, current_user
from app.tools.tools import can
main=Blueprint('main',__name__)

@main.route('/')
@login_required
def index():
    print u"{name}".format(name=current_user.username)
    return 'success '

@main.route('/cas-success')
@login_required
def success():
    if  not can(current_user.role):
        return 'hello,普通用户:'+current_user.email
    else:
        return u'管理员,'+current_user.email