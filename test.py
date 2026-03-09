from bird_kb import Node

import json

test_node = {
    "title": "United States' Bird Conservation Organization Plan 2020",
    "item_type" : "Plan",
}

class_test = Node(test_node)

print(json.dumps(class_test.__dict__, indent=2))