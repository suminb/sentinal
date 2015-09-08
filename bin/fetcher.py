
import click
from sqlalchemy.exc import IntegrityError
from newspaper import Article as NewsArticle
from konlpy.tag import Kkma
from konlpy.utils import pprint

from sentinal import create_app
from sentinal.models import db, Article as ArticleEntity, Word, \
    FLAG_TO_BE_DOWNLOADED


FLAG_EXTRACTED_KEYWORDS = 0x0001
FLAG_SENTIMENT_ANALYSIS = 0x0002

app = create_app()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
def fetch_article(url):
    article = NewsArticle(url)
    article.build()

    print(article.keywords)

    with app.app_context():
        ArticleEntity.create_from_news_article(article)


@cli.command()
def fetch_articles():
    with app.app_context():
        for article in ArticleEntity.query.filter(
                ArticleEntity.flags == FLAG_TO_BE_DOWNLOADED):

            news_article = NewsArticle(article.url)
            news_article.download()
            news_article.parse()
            news_article.nlp()

            article.publish_date = news_article.publish_date
            article.authors = '|'.join(news_article.authors),
            article.title = news_article.title
            article.text = news_article.text
            article.flags = 0

            db.session.commit()


@cli.command()
def extract_keywords():
    with app.app_context():
        kkma = Kkma()
        for article in ArticleEntity.query.filter(ArticleEntity.flags == 0):
            keywords = kkma.nouns(article.text)

            for keyword in keywords:
                click.echo('keyword {}'.format(keyword))
                try:
                    word = Word.create(word=keyword)
                except IntegrityError:
                    db.session.rollback()
                    # If duplicate is found
                    word = Word.query.filter(Word.word == keyword).first()
                article.keywords.append(word)
            article.flags |= FLAG_EXTRACTED_KEYWORDS

        db.session.commit()


@cli.command()
def create_all():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    cli()
