# -*- coding: utf-8 -*-
# @Author  : dmac


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role, Articletype, Articlesource


class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'所在地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')
    cancel = SubmitField(u'取消', render_kw={'data-dismiss': 'modal'})


class EditProfileAdminForm(EditProfileForm):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能包含字母、数字、点和下划线')],
                           render_kw={'placeholder': '6-15位字母或数字', 'autocomplete': 'off'})
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()],
                        render_kw={'placeholder': '例如:123@123.com', 'autocomplete': 'off'})
    confirmed = BooleanField(u'是否已经确认')
    role = SelectField(u'系统角色', coerce=int)

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱地址已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被注册')


class ArticleForm(FlaskForm):
    title = StringField(u'文章标题', validators=[DataRequired(), Length(1, 50, message=u"长度必须在50个字符以内")], render_kw={'placeholder': '1-50个文字', 'autocomplete': 'off'})
    article_source = SelectField(u'文章来源', coerce=int)
    article_type = SelectField(u'文章归类', coerce=int)
    abstract = TextAreaField(u'文章摘要', validators=[DataRequired(), Length(1, 150, message=u"长度必须在150个字符以内")], render_kw={'placeholder': '1-150个文字', 'autocomplete': 'off'})
    body = TextAreaField(u'文章正文', validators=[DataRequired()], render_kw={'placeholder': '写点什么吧', 'autocomplete': 'off'})
    cover = StringField(render_kw={'type': 'hidden'})
    submit = SubmitField(u'提交')
    # cancel = SubmitField(u'取消', render_kw={'data-dismiss': 'modal'})

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.article_type.choices = [(articletype.id, articletype.name) for articletype in Articletype.query.order_by(Articletype.name).all()]
        self.article_source.choices = [(articlesource.id, articlesource.name) for articlesource in Articlesource.query.order_by(Articlesource.name).all()]


class CommentFrom(FlaskForm):
    nickname = StringField(u'昵称', validators=[DataRequired(), Length(1, 50, message=u"长度必须在10个字符以内")], render_kw={'autocomplete': 'off'})
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()], render_kw={'autocomplete': 'off'})
    body = TextAreaField(u'评论内容', validators=[DataRequired()], render_kw={'autocomplete': 'off'})
    reply = StringField(validators=[DataRequired()])
    submit = SubmitField(u'提交')