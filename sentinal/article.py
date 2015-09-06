from flask import Blueprint, request, redirect, render_template, url_for

from sentinal.forms import AddUrlForm
from sentinal.models import Article, FLAG_TO_BE_DOWNLOADED

article_module = Blueprint('article', __name__)


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
