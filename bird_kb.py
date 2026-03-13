# author: Scott K. Anderson
# Purpose:
#   define classes for bird conservation knowledge base

from mongodb_conservation_connections import db
import string
import json
from jsonschema import validate, ValidationError
from datetime import datetime
import requests
import yaml

# special characters to remove from title for key
special_chars = list(string.punctuation)
nl = "\n"
# print(f"special_chars: {special_chars}")
node_schema_uri = "https://gist.githubusercontent.com/ncbirdconservation/15ac248b1679dc25145fbc741621f07f/raw/conservation_kb_node_schema.json"
response = requests.get(node_schema_uri)
node_schema = response.json()
front_matter_keys = [
    "key",
    "title",
    "type",
    "url",
    "description",
    "properties",
    "tags"
]
date_fmt = "%Y-%m-%d %H:%M:%S"



# loop through keys in dict and convert to lowercase and replace spaces with _

# def modify_dict_key(key):
#     # pass text: lowercase, replace spaces with underscores
#     return key.replace(" ", "_").lower()

# def recurse_keys(d):
#     result = {}
#     for key, value in d.items():
#         new_key = modify_dict_key(key)
#         if isinstance(value, dict):
#             # Recursively call the function for nested dictionaries
#             result[new_key] = {}
#             recurse_keys(value)
#         elif isinstance(value, list):
#             # Optionally handle lists which might contain dictionaries
#             result[new_key] = []
#             for item in value:
#                 if isinstance(item, dict):
#                     recurse_keys(item)
#                 else:
#                     result[new_key].append(item)
#         else:
#             result[new_key] = value
#     return result

# Setup connection to MongoDB
# nodes = db.kb_nodes
# edges = db.kb_edges
# crosswalk = db.kb_crosswalk
# dbs = db.kb_dbstatus

# def find_key(item):
#     # check crosswalk for disambiguation
#     return ""

# def check_data(key, type):

#     q = {"key": key}
#     p = {"_id": 0}

#     # check current KB if exists, return current record
#     if type == "node":
#         result = list(nodes.find(q, p))[0]
#     # elif type == "edge":
#     #     result = list(edges.find(q, p))[0]
#     else:
#         print("entity not edge or node")
#         pass

    # return result

class Node:
    def __init__(self, data = {}):
        self.key = ""
        # self.short_key = ""
        # self.title = ""
        # self.url = ""
        # self.type = ""
        # self.description = ""
        # self.citation = ""
        # self.aliases = []
        # self.tags = []
        # self.properties = {}
        # # self.timeline = []
        # self.page = ""
        # self.modified_date = ""
        # self.created_date = ""
        self.db_record_present = False
        self.valid = False
        self.keys_to_remove = [
            "valid",
            "keys_to_remove",
            "db_record_present",
            "db_node"
        ]

        if not (any(i in data for i in ["key", "title"])):
            print(f"Provide data with either 'key' or ('title' and 'type') values.")
        else:
            # check db for node record
            if "key" in data:
                q = {"aliases":data["key"]}
            elif "title" in data:
                q = {"aliases":data["title"]}

            if q:
                node = list(db.kb_nodes.find(q, {"_id": 0}).limit(1))
                    
                if node:
                    print(node[0])
                    self.db_record_present = True
                    self.db_node = node[0]

            # populate with passed data
            # either updates existing record, or creates new one
            self.populate(data)


        # self.populate(data)

        
    def derive_key_from_title(self):
        if not self.type:
            try:
                self.type = self.data["type"]
            except:
                self.type = "unknown"
        result = self.title.lower()

        for i in special_chars:
            result.replace(i, "")

        key_list = result.split(" ")

        ## key
        key_list.insert(0, self.type.lower())
        self.key = "-".join(key_list)

        # self.derive_short_key_from_title()
    
    # def derive_short_key_from_title(self):
    #     result = self.title.lower()

    #     for i in special_chars:
    #         result.replace(i, "")
        
    
    #     ## short key
    #     sk = ""
    #     sk_end = ""
    #     sk_key_list = result.split(" ")
    #     if sk_key_list[-1].isnumeric():
    #         # last item is likely a year or date
    #         # remove from list and append to short key
    #         sk_end = sk_key_list.pop()
        
    #     for i in sk_key_list:
    #         sk += i[0]
    
    #     self.short_key = sk + sk_end

    def validate_node(self):
        # check if current node conforms to node schema
        # hosted at:
        # https://gist.githubusercontent.com/ncbirdconservation/15ac248b1679dc25145fbc741621f07f/raw/8f85f385a529b978acee09b8085bb692c2dbb032/conservation_kb_node_schema.json

        try:
            validate(
                instance = self.export_node_record(),
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
        # formatted_data = recurse_keys(data)

        # check if key passed, if not, calculate
        if "key" not in data:
            self.type = data["type"]
            self.title = data["title"]
            self.derive_key_from_title()
        
        for k, v in data.items():
            if k != "key": setattr(self, k, v)

        if not(self.db_record_present):
            # new record, add created/modified dates
            self.created_date = datetime.now().strftime(date_fmt)
            self.modified_date = datetime.now().strftime(date_fmt)

        # validate record
        self.validate_node()

    def update_database(self):
        # check to see if current version if valid
        if self.valid:
            if self.db_record_present:
                changes = self.check_record_changes()
                if changes:
                    print("Updates found, new values:")
                    print(changes)
                    # update_existing = input(f"Update {self.title} database record (y/N)?")
                    # if update_existing.lower() == "y":
                    #     try:
                    #         db.kb_node.update_one(
                    #             {"key" : self.key},
                    #             {"$set" : changes}
                    #         )
                    #         print("updated successfully!")
                    #     except:
                    #         print("update failed.")
                else:
                    print("no changes found.")
            else: # no db record, return insert code
                new = input("No record found on database. Create a new one (y/N)?")
                if new.lower() == "y":
                    try:
                        set = self.export_node_record()
                        set.pop("key")
                        print("set code before creating new record")
                        print(json.dumps(set))
                        db.kb_node.update_one(
                            {"key" : self.key},
                            {"$set" : set}
                        )
                        print("record created!")
                    except:
                        print("record creation failed.")
        else:
            print("Record does not conform to standards.")

   
    
    def check_record_changes(self):
        # returns False if no record or no changes
        # returns dict of $set statement if changes present
        if self.db_node:
            db_node = self.db_node
            del db_node["key"]
            print("checking db node:")
            print(json.dumps(self.db_node, indent=2))

            curr_node = self.export_node_record()
            del curr_node["key"]
            print("checking curr node:")
            print(json.dumps(curr_node, indent=2))
            # check for changes, build set code if any
            if db_node == curr_node:
                print("no changes found!")
                return False
            else:
                # check for updated keys
                set = {}
                for k, v in db_node.items():
                    if k in curr_node:
                        if curr_node[k] != v:
                            # is it a dict?
                            if isinstance(v, dict):
                                #loop through and compare
                                for key, value in v.items():
                                    if key in curr_node:
                                        if curr_node[k][key] != value:
                                            set[f"{k}.{key}"] = value
                            else:
                                set[k] = v
                
                #check for curr node keys not in database
                for k, v in curr_node.items():
                    if k not in db_node:
                        set[k] = v
                    elif isinstance(v, dict):
                        for key, value in v.items():
                            if key not in db_node[k]:
                                set[f"{k}.{key}"] = value
                return set
        else:
            return False 

    def export_node_record(self):
        # returns dict of node record wihtout admin variables
        results = {}
        for key, value in self.__dict__.items():
            if key not in self.keys_to_remove:
            # if (key not in self.keys_to_remove and bool(value)):
                results[key] = value

        return results
    
    def export_to_md(self, file_path):
        # get path, build full path
        if file_path[-1] != "/": file_path += "/"
        full_path = file_path + self.key + ".md"

        # get front matter
        front_matter = {key: value for key, value in self.__dict__.items() if key in front_matter_keys}

        # write results to file
        with open(full_path, "w", encoding="utf-8-sig") as file:
            front_yaml = yaml.dump(front_matter, default_flow_style=False)
            file.write(nl.join(["---",front_yaml, "---"]))
            file.write(self.page)

    def export_to_jekyll_md(self, file_path):
        # get path, build full path
        if file_path[-1] != "/": file_path += "/"
        full_path = file_path + self.key + ".md"

        # get front matter
        front_matter = {key: value for key, value in self.__dict__.items() if key in front_matter_keys}
        front_matter["layout"] = "page"
        front_matter["published"] = "true"
        front_matter["authors"] = "NC Bird Conservation"
        front_matter["date"] = self.modified_date[:10]
        # front_matter["permalink"] = "/kb/" + self.key

        # write results to file
        with open(full_path, "w", encoding="utf-8-sig") as file:
            front_yaml = yaml.dump(front_matter, default_flow_style=False)
            file.write(nl.join(["---",front_yaml, "---"]))
            file.write(self.page)
