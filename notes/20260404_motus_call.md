---
title: "2026-04-04 NC Motus Meeting"
author: "Scott K. Anderson"
date: "2026-04-04"
type: meeting-notes
organization: "NC Motus Working Group"
frequency: "occasional"
tags: []
---

# Attendees

- Richard Gray - High Country Audubon Motus tower at ASU sustainable development farm.
- Garrett Rhyne - American Bird Conservancy
- Kendrick Weeks - NCWRC
- Chris Kelly - NCWRC
- Dana Sargent - Audubon NC
- Sara Marschhauser - Audubon NC
- Barbara Driscoll - New Hope Bird Alliance
  - Adding tower at brumley north
- Mary Abrams - Wake Audubon
  - working on capacity issues
- Page Turner - NCWF (SE) - Cape Fear Audubon
  - 3 CHSW towers in Wilmington
- Cyrenea Millberry - 
- Joe Poston - Catawba College - got grant to fund 4 towers in the piedmont

> Motus has an API that could be used to make an R dashboard

```yaml
nodes:
  project-chimney-swift-motus-tracking:
  short_key: chsw-motus
  title: Chimney Swift Motus Tracking
  type: project
  description: Project to tag ~25 Chimney Swifts.
  tags: [chimney swift, motus]
  relationships:
      chsw-motus|is_project_of|american-bird-conservancy:
        title: "American Bird Conservancy"
        key: organization-association-of-fish-and-wildlife-agencies
        verb_forward: "is committee of"
        verb_backward: "has committee"
        source: "Scott K. Anderson"
```