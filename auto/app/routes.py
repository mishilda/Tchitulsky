#-*- coding: UTF-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, MakeOrderForm
from app.logic import UserLogic, ClientLogic, DriverLogic, StoreLogic, OrderLogic
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Client, Driver, Store, Order
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
	orders=[]
	if current_user.is_authenticated:
		orders = UserLogic(current_user.id).ordersObj()
	return render_template('index.html', orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		if UserLogic().authorization(form.username.data, form.password.data, form.remember_me.data):
			return redirect(request.args.get('next') or url_for('index'))
		else: return redirect(url_for('login'))
	return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/clients')
@login_required
def clients():
	clients = ClientLogic().clients
	return render_template('client_list.html', clients=clients)

@app.route('/client/<id>')
@login_required
def client(id):
	client = ClientLogic(id).clients
	return render_template('client.html', client=client)

@app.route('/drivers')
@login_required
def drivers():
	drivers = DriverLogic().drivers
	return render_template('driver_list.html', drivers=drivers)

@app.route('/driver/<id>')
@login_required
def driver(id):
	driver = DriverLogic(id).drivers
	return render_template('driver.html', driver=driver)

@app.route('/stores')
@login_required
def stores():
	stores = StoreLogic().stores
	return render_template('store_list.html', stores=stores)

@app.route('/store/<id>')
@login_required
def store(id):
	store = StoreLogic(id).stores
	return render_template('store.html', store=store)

@app.route('/order/<id>')
@login_required
def order(id):
	order = OrderLogic(id)
	return render_template('order.html', order=order)

@app.route('/new_order', methods=['GET', 'POST'])
@login_required
def new_order():
	form = MakeOrderForm()
	form.client.choices=[(client.id, client.name) for client in UserLogic(current_user.id).clients]
	form.driver.choices=[(driver.id, driver.name) for driver in DriverLogic().drivers]
	form.store.choices=[(store.id, store.code) for store in StoreLogic().stores]
	if form.validate_on_submit():
		if OrderLogic().save(form.client.data, form.driver.data, form.store.data, form.date_to.data, form.size.data, form.weight.data, form.cost.data):
			flash('Заказ сохранен.')
			return redirect(url_for('index'))
	return render_template('makeorder.html', title='Создать заказ', form=form)

@app.route('/edit_order/<id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
	form = MakeOrderForm()                                                               
	form.client.choices=[(client.id, client.name) for client in UserLogic(current_user.id).clients]
	form.driver.choices = [(driver.id, driver.name) for driver in DriverLogic().drivers]
	form.store.choices = [(store.id, store.code) for store in StoreLogic().stores]
	
	order = OrderLogic(id)
	if form.validate_on_submit():	
		if order.save(form.client.data, form.driver.data, form.store.data, form.date_to.data, form.size.data, form.weight.data, form.cost.data):
			flash('Заказ изменен успешно!')
			return redirect(url_for('index'))
	elif request.method == 'GET':
		if type(order.clients) is not type([]):
			form.client.data = order.clients.id
		if type(order.drivers) is not type([]):
			form.driver.data = order.drivers.id
		if type(order.stores) is not type([]):
			print(order.stores)
			form.store.data = order.stores.id
		form.date_to.data = order.orders.date_to
		form.weight.data = order.orders.weight
		form.size.data = order.orders.size
		form.cost.data = order.orders.cost 
	return render_template('edit_order.html', title='Редактировать заказ', form=form, order=order)
