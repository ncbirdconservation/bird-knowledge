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
## retrieve edges, create relationships in kb_nodes

# convert edge type to proper case
def convert_edge_type(t):
    return t.replace("_", " ").title()

# download all edges
q = {}
p = {}

results = db.edges.find(q, p).limit(3)

edge_count = 0
for e in results:
    print("edge: ")
    print(e)

    # build relationship object
    rel_dict = {
        "title" : e["from"],
        "relationships" : [
            {
                "key" : "",
                "title" : e["to"],
                "verb" : convert_edge_type(e["type"])
            }
        ]
    }
    print(json.dumps(rel_dict, indent=2))
    # create node from the from field
    from_node = Node(rel_dict)   
    print(f"From node on db? {from_node.db_record_present}")
    print(json.dumps(from_node.export_node_record(), indent=2))

    edge_count += 1
    if edge_count >1: break

exit()

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