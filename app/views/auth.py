#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import time
from urllib import urlencode,urlopen
from urlparse import urljoin
from flask import current_app
from flask import redirect
from flask import request
from flask import url_for
from flask_login import login_user,login_required, logout_user
from werkzeug.contrib.cache import SimpleCache
from xmltodict import parse as xml_parse
from flask import Blueprint
from flask import session
from app.models.auth import Users
from extensions import db

cas_logout_tickets=SimpleCache()
auth=Blueprint('auth',__name__)
from extensions import csrf

@csrf.exempt
@auth.route('/login/')
def login():
    return cas_login()

def cas_login():
    if request.method=='POST':
        logout_request=request.form.get('logoutRequest')
        print logout_request
        try:
            xml_obj=xml_parse(logout_request)
            ticket=xml_obj['samlp:LogoutRequest']['samlp:SessionIndex']
            cas_logout_tickets.set(ticket,1)
        except:
            pass
        return '',200
    ticket = request.args.get('ticket')
    if ticket:
        if validate_cas(ticket):
            session['cas_ticket']=ticket
        return redirect(request.args.get('next') or url_for("main.index"))

    s=request.url
    session['cas_s']=s
    cas_query = [('service', s)]
    cas_login_url = urljoin(current_app.config['CAS_LOGIN_URL'], '?{0}'.format(urlencode(cas_query)))
    return redirect(cas_login_url)

def validate_cas(ticket):
    s=session.pop('cas_s')
    validate_query=[('service',s),('ticket',ticket)]
    from flask import current_app
    cas_validate_url=urljoin(current_app.config['CAS_TOKEN_VALIDATE_URL'],'?{0}'.format(urlencode(validate_query)))
    isValid = False
    try:
        rst_xml_obj=urlopen(cas_validate_url).read().strip()
        xml_dict=xml_parse(rst_xml_obj)
        attr = xml_dict['cas:serviceResponse']['cas:authenticationSuccess']['cas:attributes']
        isValid = True if "cas:authenticationSuccess" in xml_dict["cas:serviceResponse"] else False

    except Exception as e:
        traceback.print_exc()

    if isValid:
        xml_dict=xml_dict['cas:serviceResponse']['cas:authenticationSuccess']
        user_id=xml_dict['cas:user']
        attributes = xml_dict.get("cas:attributes", {})
        user_mail=attributes.get('cas:mail','')
        user_displayName=attributes.get('cas:displayName','')
        try:
            xing=user_displayName[0]
        except:
            xing=''
        try:
            ming=user_displayName[1:]
        except:
            ming=''

        log_user_in(user_id, xing, ming, user_mail)

    return isValid
def log_user_in(user_id,xingshi,mingzi,mail,remember_me=False):
    user = Users.query.filter_by(email=mail).first()
    (role,is_confirm) = (0,0) if user else (1,1)
    username = u'{name}'.format(name=(xingshi+mingzi))
    email = mail
    c_time=time.strftime('%Y-%m-%d %H:%M:%S')
    if not user:
        u=Users()
        u.username = username
        u.reg_time = c_time
        u.is_confirm = is_confirm
        u.role = role
        u.email = email
        db.session.add(u)
        db.session.commit()
    else:
        user.last_login = c_time
        db.session.commit()
    user=Users.query.filter_by(email=mail).first()
    login_user(user,remember=remember_me)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    cas_query = [('service', url_for('main.success', _external=True))]
    cas_logout_url = urljoin(current_app.config['CAS_LOGOUT_URL'], '?{0}'.format(urlencode(cas_query)))
    return redirect(cas_logout_url)