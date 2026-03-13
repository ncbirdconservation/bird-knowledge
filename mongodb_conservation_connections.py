
from pymongo.mongo_client import MongoClient
import certifi
from mdbconn import connString


# Setup connection to MongoDB
max_timeout = 100000000
client = MongoClient(
    connString(), 
    connectTimeoutMS=max_timeout,
    socketTimeoutMS = max_timeout,
    serverSelectionTimeoutMS=max_timeout,
    tlsCAFile=certifi.where()
    )

db = client.conservation_connections