from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<User {}>'.format(self.username)
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash,password)

	# @login.user_loader
	# def load_user(id):
	# 	return User.query.get(int(id))


class Clubs(db.Model):
	__tablename__ = 'clubs'

	id = db.Column(db.Integer, primary_key = True)
	modelName = db.Column(db.String(120))
	clubType = db.Column(db.String(120))
	brandName = db.Column(db.String(120))

	def __repr__(self):
		return '<modelName> {} >'.format(self.modelName)

class Bags(db.Model):
	__tablename__ = 'bags'

	id = db.Column(db.Integer, primary_key=True)
	bagName = db.Column(db.String(120))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	def __repr__(self):
		return '<bagName> {} >'.format(self.bagName)

class BagItem(db.Model):
	__tablename__ = 'bagitem'

	id = db.Column(db.Integer, primary_key=True)
	club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
	bag_id = db.Column(db.Integer, db.ForeignKey('bags.id'))	

	def __repr__(self):
		return '<Bag User> {} >'.format(self.bag_id)

class Locker(db.Model):
	__tablename__ = 'locker'

	id = db.Column(db.Integer, primary_key = True)
	club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __repr__(self):
		return '<Locker User {}>'.format(self.user_id)


# https://mysql.tutorials24x7.com/blog/guide-to-design-database-for-shopping-cart-in-mysql