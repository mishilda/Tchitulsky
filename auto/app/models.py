from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	name = db.Column(db.String(150))
	inn = db.Column(db.String(50))
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	clients = db.relationship('Client', backref='manager', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), index=True, unique=True)
	country = db.Column(db.String(30), index=True)
	city = db.Column(db.String(100))
	addr = db.Column(db.String(250))
	contact_person_name = db.Column(db.String(150))
	contact_person_phone = db.Column(db.String(10), index=True, unique=True)
	contact_person_email = db.Column(db.String(100), unique=True)
	phone = db.Column(db.String(10), unique=True)
	email = db.Column(db.String(100), unique=True)
	fax = db.Column(db.String(50), unique=True)
	comment = db.Column(db.String(500))
	manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))	
	orders = db.relationship('Order', backref='client', lazy='dynamic')
	
	
	def __repr__(self):
		return '<Client {}>'.format(self.name)
	
class Driver(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), index=True)
	inn = db.Column(db.String(50), unique=True)
	licence = db.Column(db.String(200))
	car = db.Column(db.String(100))
	age = db.Column(db.Integer)
	addr = db.Column(db.String(250))
	phone = db.Column(db.String(10), unique=True)
	med_licence = db.Column(db.String(100))
	med_licence_date = db.Column(db.DateTime)
	orders = db.relationship('Order', backref='driver', lazy='dynamic') 

	def __repr__(self):
		return '<Driver {}>'.format(self.name)

class Store(db.Model): #Sklad
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(10), index=True, unique=True)
	addr = db.Column(db.String(250))
	phone = db.Column(db.String(10), unique=True)
	free_place = db.Column(db.Integer) #kol-vo konteynerov
	load_place = db.Column(db.Integer)
	orders = db.relationship('Order', backref='store', lazy='dynamic')

	def __repr__(self):
		return '<Store {}>'.format(self.code)

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), index=True)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'), index=True)
	store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
	addr_from = db.Column(db.String(250))	
	addr_to = db.Column(db.String(250))
	date_from = db.Column(db.DateTime)
	date_to = db.Column(db.DateTime, index=True)
	size = db.Column(db.Integer)
	weight = db.Column(db.Float)
	cost = db.Column(db.Float)
	status = db.Column(db.String(10))

	def __repr__(self):
		return '<Order {}>'.format(self.id)