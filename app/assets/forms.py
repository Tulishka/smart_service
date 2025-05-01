import wtforms.fields.simple as field
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired


class AssetTypeForm(FlaskForm):
    name = field.StringField("Название", validators=[DataRequired()])
    description = field.TextAreaField("Описание", validators=[DataRequired()])
    image = field.FileField("Картинка (jpg/png)", validators=[FileAllowed(['jpg', 'png'])])
    submit = field.SubmitField("Сохранить")
