# http://[hostname]/api/v1.0/
#!flask/bin/python
from app import app, db
from flask import Flask, jsonify, abort, make_response, request, url_for, render_template
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from app.models import Clubs, Bags, Locker, User, BagItem


CORS(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'david':
		return 'python'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error':'Unauthorized access'}), 403)
	 # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	# Makes the Flask 404 response into JSOn rather than HTML
	return make_response(jsonify({'error':'Not found'}),404)

# Get club values in same format
def reformatClubs():
	clubs = []
	all_clubs = Clubs.query.all()

	for c in all_clubs:
		clubs.append(
			{'id':c.id,
			'modelName':c.modelName,
			'clubType':c.clubType,
			'brandName':c.brandName
			})
	return(clubs)


# def reformatBags():
# 	bags = []
# 	all_bags = Bags.query.all()

# 	for b in all_bags:
# 		bags.append(
# 			{'id':b.id,
# 			'bagName':b.bagName,
# 			'club1':b.club1,
# 			'club2':b.club2,
# 			'club3':b.club3,
# 			'club4':b.club4,
# 			'club5':b.club5,
# 			'club6':b.club6,
# 			'club7':b.club7,
# 			'club8':b.club8,
# 			'club9':b.club9,
# 			'club10':b.club10,
# 			'club11':b.club11,
# 			'club12':b.club12,
# 			'club13':b.club13,
# 			'club14':b.club14
# 			})
# 	return(bags)


#Format of db output for make_public_club and api
# clubs = [
# 	{
# 		'id': 528,
# 		'name': '905R',
# 		'type':'driver',
# 		'brand':'Titleist'

# 	},
# 	{
# 		'id': 1351,
# 		'name': 'Big Bertha 2008',
# 		'type':'driver',
# 		'brand':'Callaway'

# 	},
# 	{
# 		'id': 3358,
# 		'name': 'G400',
# 		'type':'driver',
# 		'brand':'PING'

# 	},		
# ]

db_clubs = reformatClubs()
# db_bags = reformatBags()

def make_public_club(club):
	# We're creating a new club that has all the fields except id, replacing the id field
	# with a uri
	new_club = {}
	for field in club:
		if field == 'id':
			new_club['uri'] = url_for('get_club', club_id = club['id'], _external=True)
		else:
			new_club[field] = club[field]
	return new_club


def make_public_bag(bag):

	new_bag = {}
	for field in bag:
		if field == 'id':
			new_bag['uri'] = url_for('get_bag',bag_id = bag['id'],_external=True)
		else:
			new_bag[field] = bag[field]
	return new_bag

@app.route('/api/v1.0/clubs', methods=['GET'])
# @auth.login_required
def get_clubs():
	# return jsonify({'clubs':[make_public_club(club) for club in db_clubs]})
	return jsonify({'clubs':db_clubs})
	# curl -i "http://localhost:5000/api/v1.0/clubs?clubType=putter&modelName=Zing"
	# return request.args.to_dict()
@app.route('/api/v1.0/clubs/<int:club_id>', methods=['GET'])
# @auth.login_required
def get_club(club_id):
	# Get the id of a specific club.
	# Search the club id in the clubs array.
	# If given id doesn't exist, return 404 error code.
	club = [club for club in db_clubs if club['id'] == club_id]
	if len(club) == 0:
		abort(404)
	return jsonify({'club':make_public_club(club[0])})

@app.route('/api/v1.0/clubs/<string:club_type>', methods=['GET'])
def get_clubs_by_type(club_type):
	clubs = []
	clubs_by_type = Clubs.query.filter_by(clubType=club_type).all()

	for c in clubs_by_type:
		clubs.append(
			{'id':c.id,
			'modelName':c.modelName,
			'clubType':c.clubType,
			'brandName':c.brandName
			})
	return jsonify({'clubs_by_type':[make_public_club(club) for club in clubs]})

@app.route('/api/v1.0/clubs', methods=['POST'])
# @auth.login_required
def create_club():
	# If we are missing name, type, or brand item, then we return an error code 400
	# curl -i -H "Content-Type: application/json" -X POST -d "{\"name\":\"Gap Wedge\",\"type\":\"wedge\",\"brand\":\"Kirkland\"}" http://localhost:5000/api/v1.0/clubs
	if not request.json or not 'name' or not 'type' or not 'brand' in request.json:
		abort (400)

	club = Clubs(
		modelName = request.json['name'],
		clubType = request.json['type'],
		brandName = request.json['brand']
	)
	db.session.add(club)
	db.session.flush()

	db.session.commit()
	return jsonify({'club':{'id':club.id,
			'modelName':club.modelName,
			'clubType':club.clubType,
			'brandName':club.brandName
			}}), 201

@app.route('/api/v1.0/clubs/<int:club_id>', methods=['PUT'])
# @auth.login_required
def update_club(club_id):
	# club = [club for club in db_clubs if club['id'] == club_id]
# curl -i -H "Content-Type: application/json" -X PUT -d "{"""brand""":"""KSG"""}" http://localhost:5000/api/v1.0/clubs/9592
	try:
		club = Clubs.query.get(club_id)
	except:
		club = 0

	if club == 0:
		abort(404)
	if not request.json:
		abort(400)
	# if 'name' in request.json and type(request.json['name']) != unicode:
	# 	abort(400)
	# if 'type' in request.json and type(request.json['type']) != unicode:
	# 	abort(400)
	# if 'brand' in request.json and type(request.json['brand']) != unicode:
	# 	abort(400)



	club.modelName = request.json.get('name', club.modelName)
	club.clubType = request.json.get('type', club.clubType)
	club.brandName = request.json.get('brand', club.brandName)

	db.session.flush()
	db.session.commit()

	return jsonify({'club': {'id':club.id,
			'modelName':club.modelName,
			'clubType':club.clubType,
			'brandName':club.brandName
			}})

@app.route('/api/v1.0/clubs/<int:club_id>', methods=['DELETE'])
# @auth.login_required
def delete_club(club_id):
	try:
		club = Clubs.query.get(club_id)
	except:
		club = 0

	if club == 0:
		abort(404)
	db.session.delete(club)	
	db.session.commit()
	# clubs.remove(club[0])
	return jsonify({'result':True})

@app.route('/search')
def search():
	return render_template('search.html',products=db_clubs)


#Bags
# @app.route('/api/v1.0/bags', methods=['GET'])
# # @auth.login_required
# def get_bags():
	

# 	return jsonify({'bags':[make_public_bag(bag) for bag in db_bags]})

@app.route('/api/v1.0/bags/<int:bag_id>', methods=['GET'])
# @auth.login_required
def get_bag(bag_id):
	# Get the id of a specific club.
	# Search the club id in the clubs array.
	# If given id doesn't exist, return 404 error code
	try:
		bag = BagItem.query.filter_by(bag_id=bag_id).all()
	except:
		abort(404)

	bag_clubs = []
	for club in bag:
		thisClub = Clubs.query.get(club.club_id)

		bag_clubs.append({'id':thisClub.id,
			'modelName':thisClub.modelName,
			'clubType':thisClub.clubType,
			'brandName':thisClub.brandName,
			'bag_item_id':club.id})

	return jsonify({'bag':bag_clubs})

@app.route('/api/v1.0/bags', methods=['POST'])
# @auth.login_required
def create_bag():
	# If we are missing name, type, or brand item, then we return an error code 400
	# curl -i -H "Content-Type: application/json" -X POST -d "{\"name\":\"starter\",\"user_id\":\"1\"}" http://localhost:5000/api/v1.0/bags
	if not request.json or not 'name' in request.json:
		abort (400)

	bag = Bags(
		bagName = request.json['name'],
		user_id = request.json['user_id']
	)
	db.session.add(bag)
	db.session.flush()

	db.session.commit()
	return jsonify({'bag':{'id':bag.id
			}}), 201

@app.route('/api/v1.0/bags/item', methods=['POST'])
# curl -i -H "Content-Type: application/json" -X POST -d "{"""club_id""":"""3316""","""bag_id""":"""1"""}" http://localhost:5000/api/v1.0/bags/item
def create_bag_item():
	if not request.json or not 'bag_id' in request.json:
		abort(400)
	bag_item = BagItem(
		club_id = request.json['club_id'],
		bag_id = request.json['bag_id']
		)
	db.session.add(bag_item)
	db.session.flush()
	db.session.commit()
	return jsonify({'bag_item':{'id':bag_item.id}})

@app.route('/api/v1.0/bags/item/<int:bag_item_id>', methods=['DELETE'])
def delete_bag_item(bag_item_id):
	# curl -X DELETE http://localhost:5000/api/v1.0/bags/item/3
	try:
		bag_item = BagItem.query.get(bag_item_id)
	except:
		abort(404)

	db.session.delete(bag_item)	
	db.session.commit()
	
	return jsonify({'result':True})


# Locker

@app.route('/api/v1.0/locker/<int:user_id>', methods=['GET'])
def get_locker(user_id):
# curl -i http://localhost:5000/api/v1.0/locker/1
	try:
		locker = Locker.query.filter_by(user_id=user_id).all()
	except:
		abort(404)

	locker_clubs = []
	for club in locker:

		thisClub = Clubs.query.get(club.club_id)			

		locker_clubs.append({'id':thisClub.id,
			'modelName':thisClub.modelName,
			'clubType':thisClub.clubType,
			'brandName':thisClub.brandName,
			'locker_id':club.id})

	return(jsonify({'locker': locker_clubs  }))

@app.route('/api/v1.0/locker', methods=['POST'])
# curl -i -H "Content-Type: application/json" -X POST -d "{"""club_id""":"""3316""","""user_id""":"""1"""}" http://localhost:5000/api/v1.0/locker
def create_locker():
	if not request.json or not 'club_id' in request.json:
		abort(400)
	locker = Locker(
		club_id = request.json['club_id'],
		user_id = request.json['user_id']
		)
	db.session.add(locker)
	db.session.flush()
	db.session.commit()
	return jsonify({'locker':{'id':locker.id}})

@app.route('/api/v1.0/locker/<int:locker_id>', methods=['DELETE'])
def delete_locker_item(locker_id):
	# curl -X DELETE http://localhost:5000/api/v1.0/locker/3
	try:
		locker_item = Locker.query.get(locker_id)
	except:
		abort(404)

	db.session.delete(locker_item)	
	db.session.commit()
	
	return jsonify({'result':True})


