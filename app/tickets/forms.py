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


class OpenTicketForm(FlaskForm):
    department = SelectField('Отдел', coerce=int)
    status = SelectField('Статус',
                         choices=[(status.value, status.value) for status in TicketStatus])
    result = SelectField('Результат',
                         choices=[(result.value, result.value) for result in TicketResults])
    submit = StringField('Взять/отказаться', name="action")


class ClosedTicketForm(FlaskForm):
    department = StringField('Отдел')

    status = SelectField('Статус',
                         choices=[(status.value, status.value) for status in TicketStatus])
    result = StringField('Результат')
    submit = StringField('Изменить статус', name="action")
