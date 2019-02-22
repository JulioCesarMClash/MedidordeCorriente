import flask, sys, json, datetime
from flask import request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient




app = flask.Flask(__name__)
#mongodb://www.labmovilidad.unam.mx:27017
#mongodb://localhost:27017/
try:
	client = MongoClient('mongodb://localhost:27017/', maxPoolSize=50)
	mydb = client['Raspi']

except:
	print "error", sys.exc_info()[0]
	exit(1)


app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
	return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/v1/data', methods=['POST'])
def api_in():
	try:
		content = request.get_json(silent=True)
		#print content
		idsensor = mydb.sensors.insert_many(content)
		#print idsensor
		response1 = jsonify({'status':'ok'})
		response1.status_code = 200
		return response1

	except:
		print "error", sys.exc_info()[0]
		response1 = jsonify({"error":sys.exc_info()[0]})
		response1.status_code = 500
		return response1

@app.route('/api/consult', methods=['GET'])
def api_consult():
	id_search = request.args.get('id')
	dateMin = request.args.get('fmin', default = "2018-10-12 07:00:00", type = str)
	dateMax = request.args.get('fmax', default = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), type = str)
	
	if id_search is None:
		response = jsonify({"error":"Void id"})
		response.status_code = 500
		return response
	else:
		query_condition ={"$and":[{"id":id_search}, {"fecha":{"$gte":dateMin}}, {"fecha":{"$lte":dateMax}}]}
		find = mydb.sensors.find(query_condition)

	try:
		listdoc = [] 
		for document in find:
			document.pop("_id")
			listdoc.append(document)
		
		#print listdoc
		response = jsonify(results=listdoc)
		response.status_code = 200
		return response

	except Exception as e:
		print "error", e
		response = jsonify({"error":e})
		response.status_code = 500
		return response

	


app.run(host='0.0.0.0')
