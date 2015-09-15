from flask import Blueprint, request, redirect, render_template, url_for

from sentinal.forms import AddUrlForm, ArticleForm
from sentinal.models import Article, FLAG_TO_BE_DOWNLOADED

article_module = Blueprint('article', __name__)


@article_module.route('/list')
def list_():
    """Show recent N articles."""
    articles = Article.query.order_by(Article.id).limit(15)
    context = dict(articles=articles)
    return render_template('article/list.html', **context)


@article_module.route('/<int:article_id>')
def view(article_id):
    article = Article.query.get(article_id)

    # FIXME: This should be cached
    # from konlpy.tag import Kkma
    # kkma = Kkma()
    # nouns = kkma.nouns(article.text)

    context = dict(article=article)

    return render_template('article/view.html', **context)


@article_module.route('/edit/<int:article_id>', methods=['get', 'post'])
@article_module.route('/edit/new', methods=['get', 'post'])
def edit(article_id=None):
    """Manually add/edit an article to the database. This page is probably
    unnecessary unless it provides extra functionalities that the admin
    interface does not."""
    if article_id is None:
        article = None
    else:
        article = Article.query.get(article_id)
    form = ArticleForm(request.form, obj=article)

    if form.validate_on_submit():
        # do something
        return redirect(url_for('article.edit', article_id=article_id))

    context = dict(form=form, article=article)
    return render_template('article/edit.html', **context)


@article_module.route('/add', methods=['get', 'post'])
def add():
    """FIXME: This is a temporary page for debugging."""
    article = None
    form = AddUrlForm(request.form)

    if form.validate_on_submit():
        # article = Article.create(url=form.url.data,
        #                          flags=FLAG_TO_BE_DOWNLOADED)
        from newspaper import Article as NewsArticle
        news_article = NewsArticle(form.url.data)
        news_article.build()
        Article.create_from_news_article(news_article)

        return redirect(url_for('article.add'))

    context = dict(form=form, article=article)
    return render_template('article/add.html', **context)
