import click

from newspaper import Article

from sentinal import create_app
from sentinal.models import db, Article as ArticleEntity


app = create_app()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
def fetch_article(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    print(article.keywords)

    with app.app_context():
        entity = ArticleEntity.create(
            publish_date=article.publish_date,
            title=article.title,
            text=article.text,
        )


@cli.command()
def create_all():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    cli()
