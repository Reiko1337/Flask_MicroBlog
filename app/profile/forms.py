from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from app.models import User
from flask import flash


class RegForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[Email("Некорректный Email")])
    password = PasswordField(validators=[DataRequired(), Length(min=4, message="Пароль должен быть от 4 символов")])
    confirm = PasswordField(validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Почта уже занята')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Имя пользователя занято')


class AutForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Войти')
    remember = BooleanField('Запомнить меня')


class ProfileForm(FlaskForm):
    image = FileField(validators=[DataRequired()])
    submit = SubmitField('Загрузить аватарку')

    def validate_image(self, image):
        ALLOWED_EXTENSIONS = {'jpg', 'png'}
        if image.data.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            flash('Ошибка Формата', category='error')
            raise ValidationError('Ошибка Формата')


class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    intro = TextAreaField(validators=[DataRequired()])
    text = TextAreaField(validators=[DataRequired()])
    submit_add = SubmitField('Создать')
