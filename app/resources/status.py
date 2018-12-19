import os
from flask_restplus import Namespace, Resource, fields
from flask import request
from _globals import *
from _logger import *
import requests


api = Namespace('status', description="Status of API and linked resources")

model = api.model('Status', {
	'API version': fields.String,
	'MySQL status': fields.String,
	'ElasticSearch status': fields.String,
	'LD reference panel': fields.String,
	'PLINK executable': fields.String,
	'uri': fields.Url('status_status', absolute=True)
	})
# model = api.model('Model', {
# 	'data': fields.List,
# 	'uri': fields.Url('gwas_info', absolute=True)
# 	})



@api.route('/')
@api.doc(description="Something something something")
class Status(Resource):
	@api.marshal_with(model)
	def get(self):
		logger_info()
		out = {
					'API version': VERSION,
					'MySQL status': check_mysql(),
					'ElasticSearch status': check_elastic(),
					'LD reference panel': check_ld_ref(),
					'PLINK executable': check_plink()
		}
		return out

def check_ld_ref():
	if(os.path.isfile(LD_REF+".bed") and os.path.isfile(LD_REF+".bim") and os.path.isfile(LD_REF+".fam")):
		return "Available"
	else:
		return 'Unavailable'

def check_plink():
	if os.popen(PLINK + " --version").read().split("\n")[0] == '':
		return 'Unavailable'
	else:
		return "Available"

def check_elastic():
	url = 'http://'+app_config['es']['host'] + ':' + str(app_config['es']['port']) + '/_cluster/health?pretty'
	try:
		out = requests.get(url).json()
		if out['status'] == 'red':
			return "Unavailable"
		else:
			return "Available"
	except Exception as e:
		print e
		return "Error"

def check_mysql():
	SQL   = "show databases;"
	# SQL   = "SELECT COUNT(*) FROM study_e;"
	try:
		query = PySQLPool.getNewQuery(dbConnection)
		query.Query(SQL)
		if len(query.record) > 0:
			return "Available"
		else:
			return "Unavailable"
	except Exception as e:
		print e
		return "Error"
