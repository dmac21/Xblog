# -*- coding: utf-8 -*-
# @Author  : dmac

from flask import render_template, abort, flash, redirect, url_for, request, jsonify
from . import main
from .. import db
from ..auth.forms import LoginForm, RegisterForm
from .forms import EditProfileForm, EditProfileAdminForm, ArticleForm, CommentFrom
from ..models import User, Role, Article, Articletype, Articlesource, Blogview
from flask_login import login_required, current_user
from datetime import datetime
import os
import qiniu
import os, random, string
from werkzeug.utils import secure_filename
from config import config


@main.app_context_processor
def inject_info():
    loginform = LoginForm()
    registerform = RegisterForm()
    articlesources = Articlesource.query.all()
    articletypes = Articletype.query.all()
    top5_articles = Article.query.order_by(Article.views.desc()).limit(5).all()
    total_article_count = Article.query.count()
    blogviews = Blogview.query.first()
    return dict(articlesources=articlesources, articletypes=articletypes, top5_articles=top5_articles,
                total_article_count=total_article_count, loginform=loginform, registerform=registerform, blogviews=blogviews)


@main.route('/')
def index():
    blogview = Blogview()

    blogview.add_view()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    articles = pagination.items
    return render_template('index.html', articles=articles, pagination=pagination)


@main.route('/write_article', methods=['GET', 'POST'])
@login_required
def write_article():
    articleform = ArticleForm()
    if articleform.validate_on_submit():
        body_html = request.form['xblog-editormd-html-code']
        cover = config.QINIU_DOMAIN + "/" + request.form['input-b2']
        article = Article(title=articleform.title.data, abstract=articleform.abstract.data, body=articleform.body.data,
                          articletype_id=articleform.article_type.data, articlesource_id=articleform.article_source.data,
                          body_html=body_html, cover=cover, author=current_user)
        db.session.add(article)
        db.session.commit()
        flash(u"发布文章成功！")
        return redirect(url_for('main.index'))
    return render_template('editarticle.html', articleform=articleform)


@main.route('/update_article/<int:id>', methods=['GET', 'POST'])
@login_required
def update_article(id):
    article = Article.query.filter_by(id=id).first()
    articleform = ArticleForm(title=article.title, abstract=article.abstract, body=article.body,
                              article_source=article.articlesource_id, article_type=article.articletype_id)
    if articleform.validate_on_submit():
        body_html = request.form['xblog-editormd-html-code']
        cover = config.QINIU_DOMAIN + "/" + request.form['input-b2']
        article.title = articleform.title.data
        article.abstract = articleform.abstract.data
        article.body = articleform.body.data
        article.body_html = body_html
        article.cover = cover
        article.articletype_id = articleform.article_type.data
        article.articlesource_id=articleform.article_source.data
        article.author = current_user
        article.update_timestamp = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        flash(u"更新文章成功！")
        return redirect(url_for('main.index'))
    return render_template('editarticle.html', articleform=articleform)


@main.route('/user/<username>')
@login_required
def user(username):
    editprofileform = EditProfileForm()
    user = User.query.filter_by(username=username).first()
    editprofileadminform = EditProfileAdminForm(user)
    if user is None:
        abort(404)
    articles = Article.query.filter_by(author=user).order_by(Article.timestamp.desc()).all()
    return render_template('user.html', user=user, editprofileform=editprofileform, editprofileadminform=editprofileadminform,
                           articles=articles)


@main.route('/article/<int:id>')
def article(id):
    article = Article.query.filter_by(id=id).first()
    article.add_view()
    commentform = CommentFrom()
    return render_template('article.html', article=article, commentform=commentform)


@main.route('/articletype/<int:id>')
def articletype(id):
    articletype = Articletype.query.filter_by(id=id).first()
    articles = Article.query.filter_by(articletype=articletype).order_by(Article.timestamp.desc()).all()
    return render_template('articles.html', articles=articles)


@main.route('/articlesource/<int:id>')
def articlesource(id):
    articlesource = Articlesource.query.filter_by(id=id).first()
    articles = Article.query.filter_by(articlesource=articlesource).order_by(Article.timestamp.desc()).all()
    return render_template('articles.html', articles=articles)


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


@main.route('/upload', methods=['POST'])
@login_required
def upload():
    f = request.files.get("input-b2", None) or request.files.get('editormd-image-file', None)
    if not f:
        res = {
            'success': 0,
            'message': u'图片格式异常'
        }
        return jsonify(res)
    filename = secure_filename(f.filename)
    # sfx = filename.rsplit(".")[1]
    q = qiniu.Auth(config.QINIU_AK, config.QINIU_SK)
    key = filename
    # key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) + "." + sfx
    token = q.upload_token(config.QINIU_BUCKET, key, 3600)
    ret, info = qiniu.put_data(token, key, f.read())
    if ret is not None:
        qiniu_url = config.QINIU_DOMAIN + "/" + ret['key']
        res = {
            'success': 1,
            'message': u'图片上传成功',
            'url': qiniu_url
        }
        return jsonify(res)
    else:
        res = {
            'success': 0,
            'message': u'图片上传失败'
        }
        return jsonify(res)
