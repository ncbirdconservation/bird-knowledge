---
title: "data updates doc"
date: "2025-03-12"
author: "Scott K. Anderson"
type: "data-update"
---

```yaml
nodes:
    organization-partners-in-flight-science-subcommittee:
        title: "Parners in Flight Science Subcommittee"
        key: organization-partners-in-flight-science-subcommittee
        type: Organization
        url: "https://partnersinflight.org/what-we-do/science/"
        relationships:
            pifscience|is_subcommittee_of|pif:
                title: "Partners in Flight"
                key: organization-partners-in-flight
                verb_forward: "is part of"
                verb_backward: "leads"
                source: "Scott K. Anderson"
            pifscience|is_lead_by|sarah-kendrick:
                title: "Sarah W. Kendrick"
                key: person-sarah-w-kendrick
                verb_forward: "is lead by"
                verb_backward: "leads"
                source: "Scott K. Anderson"
    person-sarah-w-kendrick:
        title: "Sarah W. Kendrick"
        type: Person
        relationships:
            sarahkendrick|is_employed_by|usfws:
                title: "United States Fish and Wildlife Service"
                key: "united-states-fish-and-wildlife-service"
                verb_forward: "is employed by"
                verb_backward: "employs"
                source: "Scott K. Anderson"
    organization-ewgpif-full-annual-cycle-subcommittee:
        title: Eastern Working Group Partners in Flight Full Annual Cycle Planning Subcommittee
        short-key: ewgpif-facct
        type: Organization
        categories: ["subcommittee"]
        relationships:
            ewgpif-facct|is led by|beckystewart:
                title: Becky Stewart
                type: Person
                verb: is led by
                source: "Scott K. Anderson"
    person-becky-stewart:
        title: Becky Stewart
        type: Person
        properties:
            title: Wildlife Biologist
        relationships:
            beckystewart|leads|ewgpif-facct:
                title: "Eastern Working Group Partners in Flight Full Annual Cycle Planning Subcommittee"
                type: Organization
                verb: leads
                source: "Scott K. Anderson"
            beckystewart|is employed by|environment-and-climate-change-canada:
                title: "Environment Climate Change Canada"
                type: Organization
                verb: is employed by
                source: "Scott K. ANderson"
    organization-environment-climate-change-canada:
        title: Environment Climate Change Canada
        type: Organization
        categories: [governmental, national]
        relationships:
            environment-climate-change-canada|has geogrphy|canada:
                title: "Canada"
                type: "Geography"
                verb: has geography
                source: "Scott K. Anderson"
            

```

