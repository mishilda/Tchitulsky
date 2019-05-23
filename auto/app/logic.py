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
			order_obj = OrderLogic(order.id)
			if order_obj.not_full():
				order_obj.set_status('Обработка')
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
			self.stores = Store.query.filter_by(id=id).first()			

class OrderLogic():
	
	def __init__(self, id=None):
		if id is None:
			self.orders = Order.query.all()
			self.new = True
		else:
			self.orders = Order.query.filter_by(id=id).first()
			self.clients = ClientLogic(id=self.orders.client_id).clients
			self.drivers = DriverLogic(id=self.orders.driver_id).drivers
			self.stores = StoreLogic(id=self.orders.store_id).stores
			self.new = False

	def save(self, client, driver, store, date_to, size, weight, cost):
		self.clients = ClientLogic(client).clients
		self.drivers = DriverLogic(driver).drivers
		self.stores = StoreLogic(store).stores
		data = [self.clients.id, self.drivers.id, self.stores.id, self.stores.addr, self.clients.addr, datetime.utcnow(), date_to, size, weight, cost,'Ожидает']
		if self.new == True:
			order = Order().insert(data)
		else:
			self.orders.update(data)
		return True
		
	def not_full(self):
		if self.clients == None or self.drivers == None or self.stores == None:
			return True
		order = self.orders
		if order.addr_from == None or order.addr_to == None or order.date_from == None or order.date_to == None or order.size == None or order.weight == None or order.cost == None or order.status == None:
			return True
		return False
	
	def set_status(self, status):
		data = [self.orders.client_id, self.orders.driver_id, self.orders.store_id, self.orders.addr_from, self.orders.addr_to, self.orders.date_from, self.orders.date_to, self.orders.size, self.orders.weight, self.orders.cost, status]
		self.orders.update(data)



		