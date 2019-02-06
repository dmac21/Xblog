# -*- coding: utf-8 -*-
# @Author  : dmac

from flask import render_template, abort, flash, redirect, url_for, request
from . import main
from .. import db
from ..auth.forms import LoginForm, RegisterForm
from .forms import EditProfileForm, EditProfileAdminForm, ArticleForm
from ..models import User, Role, Article, Articletype
from flask_login import login_required, current_user


@main.route('/')
def index():
    loginform = LoginForm()
    registerform = RegisterForm()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    articles = pagination.items
    articletypes = Articletype.query.all()
    return render_template('index.html', loginform=loginform, registerform=registerform, articles=articles, pagination=pagination, articletypes=articletypes)


@main.route('/write_article', methods=['GET', 'POST'])
@login_required
def write_article():
    articleform = ArticleForm()
    if articleform.validate_on_submit():
        body_html = request.form['xblog-editormd-html-code']
        articletype = Articletype.query.filter_by(name=articleform.article_type.data).first()
        article = Article(title=articleform.title.data, abstract=articleform.abstract.data, body=articleform.body.data,
                          articletype_id=articleform.article_type.data, body_html=body_html, author=current_user)
        db.session.add(article)
        db.session.commit()
        flash(u"发布文章成功！")
        return redirect(url_for('main.index'))
    return render_template('editarticle.html', articleform=articleform)


@main.route('/user/<username>')
@login_required
def user(username):
    editprofileform = EditProfileForm()
    articletypes = Articletype.query.all()
    user = User.query.filter_by(username=username).first()
    editprofileadminform = EditProfileAdminForm(user)
    if user is None:
        abort(404)
    articles = Article.query.filter_by(author=user).order_by(Article.timestamp.desc()).all()
    return render_template('user.html', user=user, editprofileform=editprofileform, editprofileadminform=editprofileadminform,
                           articles=articles, articletypes=articletypes)


@main.route('/article/<int:id>')
def article(id):
    article = Article.query.filter_by(id=id).first()
    return render_template('article.html', article=article)


@main.route('/articletype/<int:id>')
def articletype(id):
    articletypes = Articletype.query.all()
    articletype = Articletype.query.filter_by(id=id).first()
    articles = Article.query.filter_by(articletype=articletype).order_by(Article.timestamp.desc()).all()
    return render_template('articles.html', articles=articles, articletypes=articletypes)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash(u"你的资料已经成功修改")
        return redirect(url_for('.user', username=current_user.username))
    # form.name.data = current_user.name
    # form.location.data = current_user.location
    # form.about_me.data = current_user.about_me
    # return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash(u"你的资料已经成功修改")
        return redirect(url_for('.user', username=user.username))
    # form.name.data = current_user.name
    # form.location.data = current_user.location
    # form.about_me.data = current_user.about_me
    # return render_template('edit_profile.html', form=form)