# Bird Knowledge

Experimental knowledge graph of bird conservation initiatives, species, habitats, and practices. It uses some principles from [Foam](https://marketplace.visualstudio.com/items?itemName=foam.foam-vscode), storing data in readable/editatble markdown format, designed to make management of links and entities relatively simple.

This project is **Experimental**.

## Markdown Interpretation

Markdown documents are parsed to key/value pairs and arrays based on heading/content and unordered lists (respectively).

## Notes

The notes folder contains markdown files. These are the source data the python script will use to populate the nodes and edges documents. In addition, the python script may augment notes to improve links and readability.

Note date determines premacy of information. The `update-bird-knowledge.py` script will parse notes files ,create or update appropriate nodes and edges, and modify documents to link to appropriate nodes and edges using markdown syntax (e.g., [note template](./notes/note_template.md)).

Required Headings:
* Title
* Date
* Update Date

Recognized Headings:
* Attendees
* Action Items
* Links

## Translation

A key challenge in maintaining Knowledge Graphs is creating and maintaining connections between entities. The translation.json file will maintain relationships to entity and relationship keys by maintaining common aliases. For example:

```
    {
        "Wildlife Resources Commission" : "north-carolina-wildlife-resources-commission",
        "NCWRC" : "north-carolina-wildlife-resources-commission",
        "House Wren" : "northern-house-wren"
    }
```

## Entities

### Types
* Species
* Habitat
* Organization
* Geography
* People
* Priorities

### Properties

Each node should have a list of properties - data that does not link to another entity.


## Edges

Edges are relationships between entities, and may also have associated properties to describe the relationship. Edges are directional.