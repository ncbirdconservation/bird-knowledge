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
nl = "\n" # new line
date_fmt = "%Y-%m-%d %H:%M:%S" # date format for created/modified dates

# get node schema to ensure valid records
node_schema_uri = "https://gist.githubusercontent.com/ncbirdconservation/15ac248b1679dc25145fbc741621f07f/raw/conservation_kb_node_schema.json"
response = requests.get(node_schema_uri)
node_schema = response.json()

# front matter for jekyll md pages
front_matter_keys = [
    "key",
    "title",
    "type",
    "url",
    "description",
    "properties",
    "tags"
]

# node class
class Node:
    def __init__(self, data = {}):
        self.key = ""
        self.db_record_present = False
        self.valid = False
        self.keys_to_remove = [
            "valid",
            "keys_to_remove",
            "db_record_present",
            "db_node"
        ]

        # process init data, determine if enough info to proceed
        if not (any(i in data for i in ["key", "title"])):
            print(f"Provide data with either 'key' or ('title' and 'type') values.")
        else:
            # check db for node record
            if "key" in data:
                # add key to aliases
                q = {"aliases":data["key"]}
            elif "title" in data:
                # add title to aliases
                q = {"aliases":data["title"]}

            if q:
                # check database for node, download data to compare
                node = list(db.nodes.find(q, {"_id": 0}).limit(1))
                    
                if node:
                    print(node[0])
                    self.db_record_present = True
                    self.db_node = node[0]

            # populate with passed data
            # either updates existing record, or creates new one
            self.populate(data)
        
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
        
        # populate node with db data
        if self.db_record_present:
            for k, v in self.db_node.items():
                if k != "key" : setattr(self, k, v)

        # update node with new data
        for k, v in data.items():
            if k != "key": setattr(self, k, v)

        if not(self.db_record_present):
            # new record, add created/modified dates
            self.created_date = datetime.now().strftime(date_fmt)

        self.modified_date = datetime.now().strftime(date_fmt)

        # validate record
        self.validate_node()

    ###############################################################
    ## Database checking and update functions

    def update_database(self):
        # check to see if current version if valid
        if self.valid:
            if self.db_record_present:
                changes = self.check_record_changes()
                if changes:
                    print("Updates found, new values:")
                    print(changes)
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
        
    ###############################################################
    ## Node Export Functions

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
