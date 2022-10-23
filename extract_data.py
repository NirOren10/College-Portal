from logginner import loginner
import pymongo

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://niroren:<PASSWORD>@coportal.ewqeptv.mongodb.net/test"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = pymongo.MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['coportal']

db = get_database()
COLLEGES = db['colleges']
USERS = db['users']
LOGINS = db['logins']
CHECKLISTS = db['checklists']

for login in list(LOGINS.find()):
    college = list(CHECKLISTS.find({'_id': login['collegeID']}))[0]
    loginner(login['email'],login['password'],college['url'])