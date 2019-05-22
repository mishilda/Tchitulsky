from app import app, db
from app.models import User, Client, Driver, Store, Order

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Client': Client, 'Driver': Driver, 'Store': Store, 'Order': Order}