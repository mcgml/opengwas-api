import PySQLPool
from elasticsearch import Elasticsearch
import json
import re

VERSION = '0.2.0'


# Toggle for local vs deployed
APP_CONF = "./conf_files/app_conf.json"
PLINK = './ld_files/plink1.90'
LD_REF = './ld_files/data_maf0.01_rs'
TMP_FOLDER = './tmp/'
OAUTH2_URL = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='
USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token='
LOG_FILE = "./logs/mrbaseapi.log"
LOG_FILE_DEBUG = "./logs/mrbaseapi-debug.log"


with open(APP_CONF) as f:
	app_config = json.load(f)

dbConnection = PySQLPool.getNewConnection(**app_config['mysql'])

#connect to elasticsearch
es = Elasticsearch(
		[{'host': app_config['es']['host'],'port': app_config['es']['port']}]
)

mrb_batch='MRB'
study_batches=[mrb_batch,'UKB-a','UKB-b','UKB-c','pQTL-a','eqtl-a']

