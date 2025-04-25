from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
import wtforms.fields.simple as field
import wtforms.fields.choices as choices
from wtforms.validators import DataRequired
from wtforms import SelectMultipleField, widgets


class AssetTypeForm(FlaskForm):
    name = field.StringField("Название вида ассетов", validators=[DataRequired()])
    description = field.StringField("Описание к виду ассетов", validators=[DataRequired()])
    image = field.FileField("Картинка в jpg/png", validators=[FileAllowed(['jpg', 'png'])])
    submit = field.SubmitField("Добавить")
