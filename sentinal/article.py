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


@article_module.route('/edit/<int:article_id>', methods=['get', 'post'])
@article_module.route('/edit/new', methods=['get', 'post'])
def edit(article_id=None):
    """Manually add/edit an article to the database."""
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


@article_module.route('/add_url', methods=['get', 'post'])
def add_url():
    """FIXME: This is a temporary page for debugging."""
    article = None
    form = AddUrlForm(request.form)

    if form.validate_on_submit():
        article = Article.create(url=form.url.data,
                                 flags=FLAG_TO_BE_DOWNLOADED)

        return redirect(url_for('article.add_url'))

    context = dict(form=form, article=article)
    return render_template('article/add_url.html', **context)
