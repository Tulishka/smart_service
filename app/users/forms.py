import wtforms.fields.choices as choices
import wtforms.fields.simple as field
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, widgets
from wtforms.validators import DataRequired

from app.users.models import UserStatus


class UserForm(FlaskForm):
    """Форма пользователя"""

    phone = field.TelField("Номер телефона", validators=[DataRequired()])
    name = field.StringField("Имя", validators=[DataRequired()])
    department = choices.SelectField('Отдел', coerce=int)
    status = choices.SelectField("Статус", validators=[DataRequired()],
                                 choices=[UserStatus.ACTIVE.value, UserStatus.INACTIVE.value])
    roles = SelectMultipleField("Роли",
                                choices=[],
                                option_widget=widgets.CheckboxInput(),
                                widget=widgets.ListWidget(prefix_label=False))
    submit = field.SubmitField("Сохранить")


class DepartmentForm(FlaskForm):
    """Форма отдела"""

    name = field.StringField("Наименование", validators=[DataRequired()])
    submit = field.SubmitField("Сохранить")
