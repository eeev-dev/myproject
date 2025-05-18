from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from .models.user import User


class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(2, 100)])
    avatar = FileField('Загрузите свое фото', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
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