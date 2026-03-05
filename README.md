# Bird Knowledge

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

## TO DO

* structure this repository to adhere to Jekyll formatting
* use python script to organize into pre-formatted page structures
* develop templates for different entity types, highlighting links to other pages.
* Make this database integral with NCPIF webpage - hosted by Github in Github Pages
* Consider hiding notes from git? dynamic gitignore based on yaml possible?
    * if YAML content says to hide - add to .gitignore in python
    * PyYAML
* Themes to consdier in Jekyll: [how to install](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/adding-a-theme-to-your-github-pages-site-using-jekyll)
    * [Minima](https://jekyll.github.io/minima/)
    * [Minimal](https://pages-themes.github.io/minimal/)
    * [RetLab](https://ben.balter.com/) ([see here for installing remote themes](https://github.com/benbalter/jekyll-remote-theme))
    * [Tabler](https://www.bestjekyllthemes.com/theme/tabler-tabler/)
    * [Serif](https://www.bestjekyllthemes.com/theme/zerostaticthemes-jekyll-serif-theme/)
    * [Chirpy](https://www.bestjekyllthemes.com/theme/cotes2020-jekyll-theme-chirpy/)
* RSS Feed from website for blog posts:
    * GitHub Actions: Utilize a GitHub Action like the [RSS Feed Fetch Action](https://github.com/marketplace/actions/rss-feed-fetch-action) or FeedsFetcher to automate fetching and generating static feed files within your repository.
    * External Tools/Services: Services like openrss.org can generate a feed for GitHub Issues pages by prepending openrss.org/ to the GitHub URL. Tools like [html2rss](https://html2rss.github.io/) can also convert any website content into an RSS feed.
* [Jekyll Documentation](https://jekyllrb.com/docs/pages/)
* Ability to add link to open notes page in google docs?
    * how to get meeting notes seamlessly into other formats for sharing (e.g., word doc or google)?

## Markdown Interpretation

Markdown documents are parsed to key/value pairs and arrays based on heading/content and unordered lists (respectively).

## Notes

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

```
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
* Person
* Priorities
* Plan
* Project
* Practices (or Topics)

### Properties

Each node should have a list of properties - data that does not link to another entity.


## Edges

Edges are relationships between entities, and may also have associated properties to describe the relationship. Edges are directional.