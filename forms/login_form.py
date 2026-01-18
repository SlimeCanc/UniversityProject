# forms/login_form.py
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class DeveloperLoginForm(FlaskForm):
    password = PasswordField('Пароль разработчика', validators=[
        DataRequired(),
        Length(min=3, message='Пароль должен содержать минимум 3 символа')
    ])
    submit = SubmitField('Войти')