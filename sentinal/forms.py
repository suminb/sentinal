from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class AddUrlForm(Form):
    url = StringField('url', validators=[DataRequired()])
