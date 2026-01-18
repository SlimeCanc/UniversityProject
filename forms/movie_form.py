# forms/movie_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class MovieForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=200)])
    year = IntegerField('Год выпуска', validators=[DataRequired(), NumberRange(min=1900, max=2030)])
    genre = StringField('Жанр', validators=[DataRequired(), Length(min=1, max=100)])
    rating = FloatField('Рейтинг', validators=[DataRequired(), NumberRange(min=0, max=10)])
    duration = StringField('Продолжительность', validators=[Optional(), Length(max=50)])
    type = SelectField('Тип', choices=[
        ('movie', 'Фильм'),
        ('series', 'Сериал')
    ], validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=1000)])
    image_url = StringField('URL изображения', validators=[Optional(), Length(max=500)])

    # Стриминговые платформы
    netflix_available = BooleanField('Netflix')
    amazon_available = BooleanField('Amazon Prime')
    disney_available = BooleanField('Disney+')
    hbo_available = BooleanField('HBO Max')
    apple_available = BooleanField('Apple TV+')
    hulu_available = BooleanField('Hulu')

    submit = SubmitField('Добавить фильм')