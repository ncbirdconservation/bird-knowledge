# Bird Knowledge Project

The bird consevation world is complex. There are initiatives, government, NGO, and private groups with interests in conserving birds or the ecological systems they depend upaon.

## Purpose

Building a connected Knowledge Base/Social Network Analysis

## Challenges

* **Building**: A useful resource will contain links that were not obvious prior, and the current conservation space is vast.
* **Maintenance**: These relationships are dynamic, organizations change. Keeping the data current will be a significant challenge.

# Bird Knowledge Base

Experimental knowledge graph of bird conservation initiatives, species, habitats, plans, projects, topics, and priorities. It uses some principles from [Foam](https://marketplace.visualstudio.com/items?itemName=foam.foam-vscode), storing data in readable/editatble markdown format, designed to make management of links and entities relatively simple.

Data structure will be maintained through a python script, which will do the following:

* update a MongoDB implementation
* translate and maintain links to entities
* update notes to provide proper links to nodes
* update note YAML to reflect links

This project is **Experimental**.

## Notes

Can embed YAML in markdown - create explicit links when writing notes/plan notes

Example:

```yaml
node: north-carolina-wildlife-reources-commission
type: project-owner
attributes:
  joined: "2026-02-28"
```

## Markdown Interpretation

Markdown documents are parsed to key/value pairs and arrays based on heading/content and unordered lists (respectively).

## Notes Folder

The notes folder contains markdown files. These are the source data the python script will use to populate the nodes and edges documents. In addition, the python script may augment notes to improve links and readability.

Note date determines premacy of information. The `update-bird-knowledge.py` script will parse notes files ,create or update appropriate nodes and edges, and modify documents to link to appropriate nodes and edges using markdown syntax (e.g., [note template](notes/_note_template.md)).

### Required YAML

* title
* date - date of meeting/note
* type - meeting-notes, plan-notes, project-notes, etc.
* key - calculated key value
* hide - indicator if this note should be ignored, and not processed
* update - date the note was last processed
* edges - calculated list of nodes linked in this note

#### YAML Edge Examples

Consider whether this is necessary.

```yaml
edges:
  - to: "scott-k-anderson"
    type: "attendee"
    edge-key: "osa7098awu43ohj"
  - to: "eastern-working-group-partners-in-flight"
    type: "meeting-note"
    edge-key: "apwepoihanfn"
```

### Link Translation

Document will attempt to 

## Translation

A key challenge in maintaining Knowledge Graphs is creating and maintaining connections between entities. The translation.json file will maintain relationships to entity and relationship keys by maintaining common aliases. For example:

```yaml
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
* Person
* Priority
* Plan
* Project
* Practices (or Topics)

### Properties

Each node should have a list of properties - data that does not link to another entity.

## Edges

Edges are relationships between entities, and may also have associated properties to describe the relationship. Edges are directional.

## Example Queries

* identify the people with the most connections across divisions?
* What organizations have connections with different populations?
* 