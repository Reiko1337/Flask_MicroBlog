from flask import render_template, url_for, redirect, flash
from . import main
from app.models import Article


@main.route('/')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('main/index.html', articles=articles)


@main.route('/post/<int:id>')
def detail_post(id):
    article = Article.query.get_or_404(id)
    return render_template('main/post_detail.html', article=article)
