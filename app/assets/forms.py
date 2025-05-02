import wtforms.fields.simple as field
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from .models import AssetStatus

import app.database.model_const as mc

class AssetTypeForm(FlaskForm):
    name = field.StringField("Название", validators=[DataRequired()])
    description = field.TextAreaField("Описание", validators=[DataRequired()])
    image = field.FileField("Картинка (jpg/png)", validators=[FileAllowed(['jpg', 'png'])])
    submit = field.SubmitField("Сохранить")


class AssetForm(FlaskForm):
    name = StringField(
        'Название',
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(max=mc.NAME_LEN, message=f"Максимальная длина {mc.NAME_LEN} символов")
        ]
    )

    type_id = SelectField(
        'Вид асета',
        coerce=int,
        validators=[DataRequired(message="Выберите вид асета")]
    )

    address = StringField(
        'Адрес',
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(max=mc.TITLE_LEN, message=f"Максимальная длина {mc.TITLE_LEN} символов")
        ]
    )

    image = field.FileField("Картинка (jpg/png)", validators=[FileAllowed(['jpg', 'png'])])

    status = SelectField(
        'Статус',
        choices=[status.value for status in AssetStatus],
        coerce=str,
        validators=[DataRequired(message="Выберите статус")]
    )

    details = TextAreaField(
        'Дополнительная информация',
        validators=[
            Optional(),
            Length(max=mc.DESCR_LEN, message=f"Максимальная длина {mc.DESCR_LEN} символов")
        ]
    )

    submit = SubmitField('Сохранить')
