from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp

from .models.user import User


class RegistrationForm(FlaskForm):
    name = StringField('Фамилия И. О.', validators=[
        DataRequired(),
        Length(2, 100),
        Regexp(r'^[А-ЯЁ][а-яё]+ [А-Я]\. [А-Я]\.$', message="Введите имя в формате: Фамилия И. О.")])
    login = StringField('Логин', validators=[DataRequired(), Length(2, 20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Данное имя пользователя уже занято. Пожалуйста, выберите другое')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(2, 20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')