from flask_wtf import FlaskForm
from wtforms.fields.choices import RadioField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class OptionForm(FlaskForm):
    option = RadioField('Что бы создать заявку выберите опцию', validators=[DataRequired()])
    submit = SubmitField('Создать заявку')