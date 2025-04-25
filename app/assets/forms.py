from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
import wtforms.fields.simple as field
import wtforms.fields.choices as choices
from wtforms.validators import DataRequired
from wtforms import SelectMultipleField, widgets


class AssetTypeForm(FlaskForm):
    name = field.StringField("Название", validators=[DataRequired()])
    description = field.TextAreaField("Описание", validators=[DataRequired()])
    image = field.FileField("Картинка (jpg/png)", validators=[FileAllowed(['jpg', 'png'])])
    submit = field.SubmitField("Сохранить")
