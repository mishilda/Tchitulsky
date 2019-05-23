from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeField 
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app.logic import ClientLogic, DriverLogic, StoreLogic, UserLogic
from flask_login import current_user

class LoginForm(FlaskForm):
	username = StringField('Логин', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	remember_me = BooleanField('Запомнить меня')
	submit = SubmitField('Войти')

class Select(SelectField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.Select(multiple=False)
	
	
class MakeOrderForm(FlaskForm):
	client = SelectField('Клиент', coerce=int, validators=[DataRequired()])
	driver = SelectField('Водитель',coerce=int, validators=[DataRequired()])
	store = SelectField('Склад', coerce=int, validators=[DataRequired()])
	date_to = DateTimeField('Дата доставки', validators=[DataRequired()])
	size = StringField('Количество контейнеров', validators=[DataRequired()])
	weight = StringField('Вес', validators=[DataRequired()])
	cost = StringField('Стоимость', validators=[DataRequired()])
	submit = SubmitField('Сохранить')


	
	
		
	
	
	