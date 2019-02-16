# -*- coding: utf-8 -*-
# @Author  : dmac

from . import auth
from .. import db
from .forms import LoginForm, RegisterForm
from ..models import User
from flask import flash, redirect, request, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from ..email import send_email

@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u"用户名或者密码错误，请重新登录！")
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)
        flash(u"一封确认邮件已经发送到你的邮箱，请到邮箱查收并确认！")
        return redirect(url_for('main.index'))
    flash(u'注册信息验证不通过，请重新核对后输入！')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u"你已经成功激活你的账号，谢谢！")
    else:
        flash(u"确认链接无效或者已经过期")
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账户', 'auth/email/confirm', user=current_user, token=token)
    flash(u"新一封确认邮件已经发送到你的邮箱，请到邮箱查收并确认！")
    return redirect(url_for('main.index'))


