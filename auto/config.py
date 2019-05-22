import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):

	POSTGRES = {
		'user':'postgres',
		'pw':'123',
		'db':'Auto',
		'host':'localhost',
		'port':'5432',
}

	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = 'postgres://postgres:123@localhost:5432/Auto'
	SQLALCHEMY_TRACK_MODIFICATIONS = False