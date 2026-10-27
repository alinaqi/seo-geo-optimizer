---
type: llm
focus: trace
weight: 1
---

The review identifies that app/page.tsx renders its main content client-side after a fetch so AI crawlers that do not execute JavaScript see an empty shell, and proposes server-side rendering or static generation
