# author: Scott K. Anderson
# Purpose:
#   define classes for bird conservation knowledge base

from pymongo.mongo_client import MongoClient
import certifi
from mdbconn import connString
import string
import json
from jsonschema import validate, ValidationError
from datetime import datetime
import requests

# special characters to remove from title for key
special_chars = list(string.punctuation)
# print(f"special_chars: {special_chars}")
node_schema_uri = "https://gist.githubusercontent.com/ncbirdconservation/15ac248b1679dc25145fbc741621f07f/raw/8f85f385a529b978acee09b8085bb692c2dbb032/conservation_kb_node_schema.json"
response = requests.get(node_schema_uri)
node_schema = response.json()
# with open("conservation_kb_node_schema.json", "r", encoding="utf-8-sig") as file:
#     # print(file.read())
#     node_schema_uri = json.load(file)


date_fmt = "%Y-%m-%d %H:%M:%S"

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
nodes = db.kb_nodes
edges = db.kb_edges
crosswalk = db.kb_crosswalk
dbs = db.kb_dbstatus

def find_key(item):
    # check crosswalk for disambiguation
    return ""

def check_data(key):
    key_parts = key.split("-")
    entity_type = key_parts[0]

    q = {"key": key}
    p = {"key": 1, "_id": 0}

    # check current KB if exists, return current record
    if entity_type == "node":
        result = list(nodes.find(q, p))[0]
    elif entity_type == "edge":
        result = list(edges.find(q, p))[0]
    else:
        pass


    return ""

class Node:
    def __init__(self, data = {}):
        self.key = ""
        self.short_key = ""
        self.title = ""
        self.url = ""
        self.item_type = ""
        self.description = ""
        self.citation = ""
        self.tags = []
        self.properties = {}
        # self.timeline = []
        self.page = ""
        self.modified_date = ""
        self.created_date = ""
        self.valid = False
        self.keys_to_remove = [
            "valid",
            "keys_to_remove"
        ]

        self.populate(data)

    def node_record(self):
        
        return {key: value for key, value in self.__dict__.items() if key not in self.keys_to_remove}
    
    def derive_key_from_title(self):
        if not self.item_type:
            try:
                self.item_type = self.data["type"]
            except:
                self.item_type = "unkown"
        result = self.title.lower()

        for i in special_chars:
            result.replace(i, "")

        ## short key
        key_list = result.split(" ")
        sk = ""
        sk_end = ""
        sk_key_list = key_list
        if sk_key_list[-1].isnumeric():
            # last item is likely a year or date
            # remove from list and append to short key
            sk_end = sk_key_list.pop()
        
        for i in sk_key_list:
            sk += i[0]
        
        self.short_key = sk + sk_end

        ## key
        key_list.insert(0, self.item_type.lower())
        self.key = "-".join(key_list)
    
    def validate_node(self):
        # check if current node conforms to node schema
        # hosted at:
        # https://gist.githubusercontent.com/ncbirdconservation/15ac248b1679dc25145fbc741621f07f/raw/8f85f385a529b978acee09b8085bb692c2dbb032/conservation_kb_node_schema.json

        try:
            validate(
                instance = self.node_record(),
                schema = node_schema
            )
            self.valid = True
            return True
        
        except ValidationError as e:
            print("The node does not conform to standards.")
            print(e.message)
            self.valid = False
            return False

    
    def populate(self, data):
        # fill in data from passed json

        # loop through items, populate node
        for k, v in data.items(): setattr(self, k, v)

        # check if key passed, if not, calculate
        if len(self.key) == 0:
            self.derive_key_from_title()
            print(f"key from title: {self.key}, short_key: {self.short_key}")

        # check if node exists in database, load current version
        # results = check_data(self.key)
        # doesn't exist, add created date
        self.created_date = datetime.now().strftime(date_fmt)
        self.modified_date = datetime.now().strftime(date_fmt)

        # validate record
        self.validate_node()

        # if exists, run update function

    def update_local(self, update_data):
        # function to update data from passsed json
        # return list of changes

        return ""

    def update_database(self):
        # update current record with local copy

        # check to see if current version if valid

        # check/update crosswalk with new info (if needed)
    
        return ""
    
    def export(self):
        # export node in json format
        pass