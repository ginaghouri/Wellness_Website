
from pymongo import MongoClient
from models import MongoDBConn, Journal
from flask import Flask


# database and collection setup.
client = MongoClient('mongodb://localhost:27017/')
chilldb = client['chillpill']
instance = chilldb['log']

# setup flask server.
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chillpill'

# send the app to the MongoDB and Journal.
mongo_conn = MongoDBConn(app)
journal = Journal(mongo_conn)
