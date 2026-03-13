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
```

