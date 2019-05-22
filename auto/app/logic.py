from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from app.models import User, Client, Driver, Store, Order
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from datetime import datetime

class UserLogic():

	
	def __init__(self, id=None):
		if id is None:
			self.users = User.query.all()
		else: 
			self.users = User.query.filter_by(id=id).first()
			self.clients = self.users.clients.all()
			self.orders = []
			for client in self.clients:
				orders = client.orders.all()
				for order in orders:
					self.orders.append(order)
			
	def set_password(self, user, password):
		user.password_hash = generate_password_hash(password)

	def check_password(self, user, password):
		return check_password_hash(user.password_hash, password)

	def authorization(self, username, password, remember_me):
		for user in self.users:
			if user.username == username and self.check_password(user, password):
				login_user(user, remember=remember_me)
				return True
		flash('Некорректный логин и/или пароль!')
		return False
		
	def ordersObj(self):
		Obj = []
		for order in self.orders:
			Obj.append(OrderLogic(order.id))
		return Obj	
		 	

class ClientLogic():
	def __init__(self, id=None):
		if id is None:
			self.clients = Client.query.all()
		else:
			self.clients = Client.query.filter_by(id=id).first()

class DriverLogic():
	def __init__(self, id=None):
		if id is None:
			self.drivers = Driver.query.all()
		else:
			self.drivers = Driver.query.filter_by(id=id).first()

class StoreLogic():
	def __init__(self, id=None):
		if id is None:
			self.stores = Store.query.all()
		else:
			self.stores = Store.query.filter_by(id=id)			

class OrderLogic():
	
	def __init__(self, id=None):
		if id is None:
			self.orders = Order.query.all()
		else:
			self.orders = Order.query.filter_by(id=id).first()
			self.clients = ClientLogic(id=self.orders.client_id).clients
			self.drivers = DriverLogic(id=self.orders.driver_id).drivers
			self.stores = StoreLogic(id=self.orders.store_id).stores

	def save(client, driver, store, date_to, size, weigth, cost):
		order = Order(client_id=client.id, driver_id=driver.id, store_id=store.id, addr_from=store.addr, addr_to=client.addr, date_from=datetime.utcnow(), date_to=date_to, size=size, weight=weight, cost=cost, status='Ожидает')
		db.session.add(order)
		db.session.commit()
		return True	



		