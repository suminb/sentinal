from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.orm import model_form

from sentinal.models import db, Article


class AddUrlForm(Form):
    url = StringField('url', validators=[DataRequired()])


# Dynamically create a form class from a model class
ArticleForm = model_form(Article, db_session=db, base_class=Form)
