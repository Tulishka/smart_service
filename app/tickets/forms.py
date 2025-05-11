from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields.choices import RadioField
from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.database import model_const as mc
from app.tickets.models import TicketStatus, TicketResults


class OptionForm(FlaskForm):
    option = RadioField('Что бы создать заявку выберите опцию', validators=[DataRequired()])
    description = TextAreaField(
        'Дополнительные сведения',
        validators=[
            Optional(),
            Length(max=mc.DESCR_LEN, message=f"Максимальная длина {mc.DESCR_LEN} символов")
        ]
    )
    submit = SubmitField('Создать заявку')


class TicketForm(FlaskForm):
    department = SelectField('Отдел', coerce=int, validators=[DataRequired()])
    status = SelectField('Статус',
                         choices=[(status.value, status.value) for status in TicketStatus],
                         validators=[DataRequired()])
    result = SelectField('Результат',
                         choices=[(result.value, result.value) for result in TicketResults],
                         validators=[DataRequired()])
    submit = StringField('Взять/отказаться', name="action")
