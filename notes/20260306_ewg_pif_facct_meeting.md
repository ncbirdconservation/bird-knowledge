---
title: "2026-03-06 EWG PIF FACCT Meeting"
author: "Scott K. Anderson"
date: "2026-03-06"
type: meeting-notes
organization: "Partners in Flight Eastern Working Group"
tags: []
attendees: 
  - Jocelynn Marriott
  - Scott Anderson
  - Bill DeLuca (National Audubon Society)
  - Meghan Sadlowski (USFWS)
    - project - Data Management/Decision Support Tool
    - project - APAC
  - Becky Stewart
  - Ted Cheskey (Nature Canada)
  - Jill Liner (National Audubon Society Vermont)
  - Randy Dettmers (USFWS)
  - David Mizrahi ()
  - Troy Wilson ()
  - Sarah Kendrick (USFWS)
  - Deb Hahn (AFWA)
  - Bob Fisher (Bird Conservation Network)
  - Guy Foulks (USFWS)
  - Patrick Devers
  - Scott Johnson
---

# Meeting Notes

## Introductions

* Who they are and where they work
* Their organization’s interest in full annual cycle conservation, e.g., what are your priority projects related to full annual cycle conservation or what do you want to be working on
* What areas would you like to collaborate on and/or why do you come to the full annual cycle conservation team meetings and what are you hoping to get out of them
* What topics/projects would you like to see the full annual cycle team take on
* What structure would you like to see for the group (e.g., have a core planning team and topic-oriented subcommittees)
(if these questions don’t work for you then tell us what you think is most important for the group to know and why)


* David Mizrahi - tagging work
  * applied for Tier 1 grant for PRAW WG
  * working with BirdsCaribbean - also winter in Central America


```yaml
nodes:
  project-APAC:
    title: APAC
  project-environmental-conservation-online-system:
    title: Environmental Conservation online System
    type: project
    subtype: [database]
    url: "https://ecos.fws.gov/ecp/"
    description: "" 
    properties:
      links:
        Species Data Explorer Home Page: "https://ecos.fws.gov/ecp/report/adhocDocumentation?catalogId=species&reportId=recoveryDocs"
        Species Data Explorer API: "https://ecos.fws.gov/ecp/report/adhocCreator?catalogId=species&reportId=recoveryDocs"

  project-information-for-planning-and-consultation:
    title: Information for Planning and Consultation
    type: project
    subtypes: 
      - resource
    description: "Quickly and easily identify USFWS managed resources and suggested conservation measures for your project. There are three main functions: Explore species and habitat, Conduct a regulatory review, and build a consultation package."
  project-information-for-planning-and-consultation:
    title: Information for Planning and Consultation
    type: project
    subtypes: 
      - resource
    description: "Quickly and easily identify USFWS managed resources and suggested conservation measures for your project. There are three main functions: Explore species and habitat, Conduct a regulatory review, and build a consultation package."
    properties:
      links:
        IPaC Location API: "https://ipac.ecosphere.fws.gov/location/api"
        IPaC API FAQ: "https://ipac.ecosphere.fws.gov/#faq"
  person-david-mizrahi:
    title: David Mizrahi
    tags: 
      - Golden-Winged Warblers
      - Prairie Warblers
      - Gray Catbirds
      - Shorebirds
      - tagging
edges:
  usfws-owns-ipac:
    from: project-information-for-planning-and-consultation
    to: organization-united-states-fish-and-wildlife-service
    direction: ["owns", "is owned by"]

```