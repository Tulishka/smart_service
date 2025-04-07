from flask_wtf import FlaskForm
from wtforms import TelField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

REQUIRED_FIELD_MESSAGE = "Обязательное поле!"


class LoginForm(FlaskForm):
    phone = TelField("Номер телефона", validators=[DataRequired(message=REQUIRED_FIELD_MESSAGE)])
    password = PasswordField("Пароль", validators=[
        DataRequired(message=REQUIRED_FIELD_MESSAGE), Length(min=5, message="Не менее 5 символов")
    ])
    remember_me = BooleanField("Запомнить меня", default=False)

    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    phone = TelField("Номер телефона", validators=[DataRequired(message=REQUIRED_FIELD_MESSAGE)])
    name = StringField("Имя", validators=[DataRequired(message=REQUIRED_FIELD_MESSAGE)])
    password = PasswordField("Пароль", validators=[
        DataRequired(message=REQUIRED_FIELD_MESSAGE), Length(min=5, message="Не менее 5 символов")
    ])
    password_again = PasswordField("Пароль", validators=[
        DataRequired(message=REQUIRED_FIELD_MESSAGE), Length(min=5, message="Не менее 5 символов")
    ])
    submit = SubmitField("Зарегистрироваться")
