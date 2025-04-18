from flask_wtf import FlaskForm
import wtforms.fields.simple as field
import wtforms.fields.choices as choices
from wtforms.validators import DataRequired, Length
from wtforms import SelectMultipleField, widgets

from app.users.models import UserStatus


class UserForm(FlaskForm):
    phone = field.TelField("Номер телефона", validators=[DataRequired()])
    name = field.StringField("Имя", validators=[DataRequired()])
    status = choices.SelectField("Статус", validators=[DataRequired()], choices=[UserStatus.ACTIVE.value, UserStatus.INACTIVE.value])
    roles = SelectMultipleField("Роли",
                              choices=[],
                              option_widget=widgets.CheckboxInput(),
                              widget=widgets.ListWidget(prefix_label=False))
    submit = field.SubmitField("Сохранить")
