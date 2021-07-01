from app import app, db
from app.models import Clubs
from app.routes import *

# send a request as you type and receive data back


def search(search_term):
	hybrids = Clubs.query.filter_by(clubType="hybrid").all()

	# search_term = "g3"
	results = []

	for c in hybrids:
		if search_term in c.modelName.lower():
			results.append([c.modelName,hybrids.index(c),c.id])

	return(results)


	# Results are a [[result, index], [result, index]]
	# so then can use index to return link to resource