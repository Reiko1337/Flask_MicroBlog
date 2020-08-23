from . import profile
from flask import render_template, redirect, url_for, flash, request
from app import db, login_manager
from .forms import RegForm, AutForm, ProfileForm, PostForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from manage import app
from app.models import Article, User


@profile.route('/reg', methods=['POST', 'GET'])
def reg():
    form = RegForm()

    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data,
                        password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно', category='success')
            if current_user.is_authenticated:
                return redirect(url_for('.logout'))
            return redirect(url_for('.aut'))
        except:
            db.session.rollback()
            flash('Ошибка в регистрации', category='error')
    return render_template('profile/reg.html', form=form)


@profile.route('/aut', methods=['POST', 'GET'])
def aut():
    form = AutForm()
    if current_user.is_authenticated:
        return redirect(url_for('.user_profile'))
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('.user_profile'))
        flash('Неверное имя пользователя или пароль', category='error')

    return render_template('profile/aut.html', form=form)


@profile.route('/Profile')
@login_required
def user_profile():
    form_profile = ProfileForm()
    form_post = PostForm()
    return render_template('profile/profile.html', form=form_profile, form_post=form_post)


@profile.route('/post/<int:id>/del', methods=['GET', 'POST'])
@login_required
def del_post(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Ошибка удаления', category='error')
    return redirect(url_for(".user_profile"))


@profile.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    try:
        article = Article.query.get_or_404(id)
        form_post = PostForm(title=article.title, intro=article.intro, text=article.text)
        if form_post.validate_on_submit():
            article.title = form_post.title.data
            article.intro = form_post.intro.data
            article.text = form_post.text.data
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('.user_profile'))
    except:
        db.session.rollback()
        flash('Ошибка редактирования', category='error')
    return render_template('profile/post_update.html', form_post=form_post, article=article)


@profile.route('/post_create', methods=['GET', 'POST'])
@login_required
def post_create():
    form_post = PostForm()
    if form_post.validate_on_submit():
        try:
            db.session.add(Article(title=form_post.title.data, intro=form_post.intro.data,
                                   text=form_post.text.data, user_id=current_user.id))
            db.session.commit()
        except:
            db.session.rollback()
            flash('Ошибка добавления поста', category='error')
    return redirect(url_for('.user_profile'))


@profile.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.aut'))


@profile.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = ProfileForm()
    try:
        if form.validate_on_submit():
            file = form.image.data
            if file:
                user = db.session.query(User).get_or_404(current_user.get_id())
                user.image = file.read()
                db.session.add(user)
                db.session.commit()
    except:
        db.session.rollback()
        flash('Ошибка добавления аватарки', category='error')
    return redirect(url_for('.user_profile'))


@profile.route('/userava')
@login_required
def userava():
    try:
        img = db.session.query(User).get_or_404(current_user.get_id()).image
        if not img:
            with profile.open_resource(app.root_path + url_for('static', filename='images/default.jpg')) as f:
                img = f.read()
        return img
    except:
        flash('Ошибка загрузки аватаки', category='error')
    return ''
