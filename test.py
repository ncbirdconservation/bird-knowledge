from bird_kb import Node
from mongodb_conservation_connections import db
import json

nl = "\n"

priority_crosswalk = {
"aos60_code" : "AOS60 Code",
"genus" : "Genus Taxonomy",
"aos59_code" : "AOS59 Code",
"audubon_conservation_plan" : "Audubon Conservation Plan",
"nc_sgcn" : "NC SGCN",
"nc_wintering" : "NC Wintering",
"bird_group" : "Bird Group",
"species_taxonomy" : "Species Taxonomy",
"family" : "Family Taxonomy",
"text" : "Text",
"order" : "Order Taxonomy",
"aos4_code" : "AOS4 Code",
"nc_breeding" : "NC Breeding",
"ebird_code" : "eBird Code",
"pif_pop_est" : "PIF Population Estimate",
"nc_state_status" : "NC State Status",
"nc_wap_evaluated" : "NC WAP Evaluated",
"aos6_code" : "AOS6 Code",
"audubon_priority" : "Audubon Priority",
"nc_management_concern" : "NC WAP Management Concern",
"publication_date" : "Publication Date",
"year" : "Year",
"community_type" : "Community Type",
"publication_year" : "Publication Year",
"priority_type" : "Priority Type",
"usfws_bcc_2021" : "USFWS BCC 2021",
"nc_wap2015_id" : "NC WAP 2015 ID",
"reference" : "Reference",
"project_status" : "Project Status",
"avibase_code" : "Avibase Code",
"classification_system" : "Classification System",
"scientific_name" : "Scientific Name",
"management_need" : "Management Need",
"nc_present" : "NC Present",
"concept" : "Concept",
"primary_author_organization" : "Primary Author Organization",
"pif_half_life" : "PIF Half Life",
"federal_status" : "Federal Listing Status",
"common_name" : "Common Name",
"threat" : "Threat",
"nc_knowledge_concern" : "NC WAP Knowledge Concern",
"ncwap15_index" : "NC WAP 2015 Index",
"hasUrl" : "URL",
"phenology" : "Phenology",
"species_group" : "Species Group",
" Has Geography" : "Geography",
" Has Scope Of" : "Scope Of",
"Has AOS4 Code" : "AOS4 Code",
"Has AOS59 Code" : "AOS59 Code",
"Has AOS6 Code" : "AOS6 Code",
"Has AOS60 Code" : "AOS60 Code",
"Has Audubon Conservation Plan" : "Audubon Conservation Plan",
"Has Avibase Code" : "Avibase Code",
"Has Bird Group" : "Bird Group",
"Has Common Name" : "Common Name",
"Has Community Type" : "Community Type",
"Has eBird Code" : "eBird Code",
"Has Family" : "Family Taxonomy",
"Has Federal Status" : "Federal Listing Status",
"Has Genus" : "Genus Taxonomy",
"Has Geography" : "Geography",
"Has Habitat" : "Habitat",
"Has Management Need" : "NC WAP 2015 Management Concern",
"Has Managment Need" : "NC WAP 2015 Management Concern",
"Has NCWAP15 Index" : "NC WAP 2015 Index",
"Has Order" : "Order Taxonomy",
"Has Organization" : "Organization",
"Has Partner" : "Partner",
"Has Phenology" : "Phenology",
"Has PIF Half Life" : "PIF Half Life",
"Has PIF Pop Est" : "PIF Population Estimate",
"Has Plan" : "Plan",
"Has Primary Author Organization" : "Primary Author Organization",
"Has Priority Type" : "Priority Type",
"Has Project Status" : "Project Status",
"Has Publication Date" : "Publication Date",
"Has Publication Year" : "Publication Year",
"Has Scientific Name" : "Scientific Name",
"Has Species" : "Species",
"Has Species Group" : "Species Group",
"Has Species Taxonomy" : "Species Taxonomy",
"Has State Status" : "NC State Status",
"Has Text" : "Text",
"Has Threat" : "Threat",
"Has WAP15 ID" : "NC WAP 2015 ID",
"Has Year" : "Year",
"Is Audubon Priority" : "Audubon Priority",
"Is NC Present" : "NC Present",
"Is SGCN" : "SGCN",
"Is WAP Knowledge Concern" : "NC WAP 2015 Knowledge Concern",
"Is WAP Management Concern" : "NC WAP 2015 Management Concern",
"Present Breeding" : "NC Breeding",
"Present Wintering" : "NC Wintering",
"Was WAP Evaluated" : "NC WAP 2015 Evaluated"
}

###########################################################
## add key and title to alias array for all nodes

# nodes = db.kb_nodes.find({},{"_id": 0, "title": 1, "key": 1})

# for n in nodes:
#     aliases = list(n.values())
#     print(f"aliases: {aliases}")
#     q = {"key": n["key"]}
#     u = {"$set" : {"aliases": aliases}}
#     db.kb_nodes.update_one(q, update=u, upsert=True)

# exit()

###########################################################
## retrieve add missing nodes from vertices in kb_nodes
# download all vertices
# load from file
with open("assets/conservation_connections.kb_nodes.json", "r", encoding="utf-8-sig") as file:
    kb_nodes = json.load(file)

out_json = []

q = {}
p = {}
results = db.vertices.find(q, p)
for v in results:
    
    q = {"title": v["title"]}
    print(f"== Checking for {v['title']} ==", nl)

    # update
    # links -> properties
    # wikitext -> page
    # categories -> categories

    node_record = {
        "title" : v["title"],
        "type" : v["type"],
        "properties" : {}
    }
    if "wikitext" not in v: 
        node_record["page"] = ""
    else:
        node_record["page"] = v["wikitext"]

    if "properties" in v:
        # loop through and fix keys
        for key, value in v["properties"].items():
            node_record["properties"][priority_crosswalk[key]] = value

    if ("links" in v and v["links"]):
        node_record["properties"]["links"] = v["links"]

    new_node = Node(data = node_record)
    # print(f"DB record present: {new_node.db_record_present}")
    # print(json.dumps(new_node.export_node_record(), indent=2))

    out_json.append(new_node.export_node_record())


    # new_node.update_database()

    # if input("Continue (y/N)?").lower() != "y":
    #     break

with open("assets/updated_kb_nodes.json", "w", encoding="utf-8-sig") as file:
    file.write(json.dumps(out_json, indent=2))

exit()

###########################################################


###########################################################
## retrieve edges, create relationships in kb_nodes

# # download all edges
# q = {}
# p = {}

# results = db.edges.find(q, p).limit(10)

# edge_count = 0
# for i in results:
#     print(f"edge: {i}")

#     # get to/from entities from kb_nodes
#     q = {"title": {"$in" : [i["from"], i["to"]]}}
#     p = {"type": 1, "key": 1, "title": 1}

#     matching_nodes = db.kb_nodes.find(q, p)
#     for n in matching_nodes:
#         print(f"node: {n}")

#     edge_count += 1
#     if edge_count >1: break

# exit()

###########################################################





# Get test nodes from JSON
with open(
    "assets/conservation_connections.nodes.json",
    "r",
    encoding = "utf-8-sig"
    ) as file:
    test_nodes = json.load(file)


node_count = 0
for n in test_nodes:
    
    class_test = Node(n)
    class_test.export_to_jekyll_md("nodes")

    # print(json.dumps(class_test.__dict__, indent=2))

    node_count += 1

    if node_count >10:
        break