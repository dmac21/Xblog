# -*- coding: utf-8 -*-
# @Author  : dmac

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired()], render_kw={'autocomplete': 'off'})
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    login = SubmitField(u'登录')
    cancel = SubmitField(u'取消', render_kw={'data-dismiss': 'modal'})


class RegisterForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能包含字母、数字、点和下划线')],
                           render_kw={'placeholder': '6-15位字母或数字', 'autocomplete': 'off'})
    password = PasswordField(u'密码', validators=[DataRequired(), EqualTo('password2', message=u'两次输入的密码必须一致')],
                             render_kw={'placeholder': '至少6位字母或数字'})
    password2 = PasswordField(u'再次输入密码', validators=[DataRequired()], render_kw={'placeholder': '至少6位字母或数字'})
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()],
                        render_kw={'placeholder': '例如:123@123.com', 'autocomplete': 'off'})
    register = SubmitField(u'注册')
    cancel = SubmitField(u'取消', render_kw={'data-dismiss': 'modal'})

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱地址已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被注册')