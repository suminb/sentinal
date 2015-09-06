from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import ARRAY

import uuid64


db = SQLAlchemy()


class CRUDMixin(object):
    """Copied from https://realpython.com/blog/python/python-web-applications-with-flask-part-ii/
    """  # noqa

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)

    @classmethod
    def create(cls, commit=True, **kwargs):
        kwargs.update(dict(id=uuid64.issue()))
        instance = cls(**kwargs)

        if hasattr(instance, 'timestamp') \
                and getattr(instance, 'timestamp') is None:
            instance.timestamp = datetime.utcnow()

        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def exists(cls, **kwargs):
        row = cls.query.filter_by(**kwargs).first()
        return row is not None

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def serialize(self, attributes=[], excludes=[]):
        """
        Serialize an instance as a dictionary
        Copied from http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
        :param attributes: Additional attributes to serialize
        """
        convert = dict()
        # add your coversions for things like datetime's
        # and what-not that aren't serializable.
        d = dict()
        for c in self.__table__.columns:
            if c.name not in excludes:
                v = getattr(self, c.name)
                if c.type in convert.keys() and v is not None:
                    try:
                        d[c.name] = convert[c.type](v)
                    except:
                        d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
                elif v is None:
                    d[c.name] = str()
                else:
                    d[c.name] = v

        for attr in attributes:
            d[attr] = getattr(self, attr)

        return d


article_word_assoc = db.Table(
    'article_word_assoc',
    db.Column('article_id', db.BigInteger, db.ForeignKey('article.id')),
    db.Column('word_id', db.BigInteger, db.ForeignKey('word.id'))
)


FLAG_TO_BE_DOWNLOADED = 0x0004

class Article(db.Model, CRUDMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    authors = db.Column(db.String)
    publish_date = db.Column(db.DateTime(timezone=False))
    url = db.Column(db.String, unique=True)
    title = db.Column(db.String)
    text = db.Column(db.Text)
    flags = db.Column(db.Integer)
    keywords = db.relationship('Word', secondary=article_word_assoc,
                               backref='article', lazy='dynamic')


class Word(db.Model, CRUDMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    word = db.Column(db.String, unique=True)
    language = db.Column(db.String(10))

# We also need a web page fetcher and a URL extractor but we probably want to
# make them as an independent module
