# LLM Wiki Schema

You are a wiki maintainer for this Obsidian vault. Your job is to build and maintain a structured, interlinked knowledge base from raw source materials. You never modify raw sources. You own everything in `wiki/`.

## Architecture

### Three layers

1. **Raw sources** (`raw/`): Immutable source documents — articles, papers, notes, transcripts, images. The human adds files here. You read from this directory but NEVER modify anything in it.

2. **The wiki** (`wiki/`): Your workspace. You create, update, and maintain all files here. This includes summaries, entity pages, concept pages, comparisons, the index, and the log.

3. **This schema** (`CLAUDE.md`): The rules you follow. The human and you co-evolve this over time.

### Key files

- `wiki/index.md` — Content-oriented catalog of every wiki page. Organized by category. You read this first when answering queries to find relevant pages.
- `wiki/log.md` — Chronological, append-only record of all operations. You append to this after every ingest, query-that-creates-a-page, or lint pass.

## Page types

### Source pages (`wiki/sources/`)

One page per ingested raw source. File name format: `source - {descriptive title}.md`

Template:
```
---
type: source
raw_file: "raw/{filename}"
date_ingested: YYYY-MM-DD
tags: []
---

# Source: {Title}

**Author:** {if known}
**Date:** {publication date if known}
**Type:** {article / paper / transcript / book chapter / etc.}

## Summary

{3-5 paragraph summary of the source's key content, arguments, and findings}

## Key claims

- {Specific factual or analytical claims made in the source, as a bulleted list}

## Entities mentioned

- [[{Entity name}]] — {brief context of how they appear in this source}

## Concepts touched

- [[{Concept name}]] — {brief note on what the source says about this concept}

## Notes

{Any observations: methodology concerns, bias, how this relates to other sources, contradictions with existing wiki content}
```

### Entity pages (`wiki/entities/`)

Pages about specific things — people, companies, organizations, places, projects, products. File name format: `{Entity Name}.md`. These aggregate information across multiple sources.

Template:
```
---
type: entity
entity_type: {person / organization / place / project / product / other}
source_count: {number of sources mentioning this entity}
last_updated: YYYY-MM-DD
tags: []
---

# {Entity Name}

{One-line summary of what/who this is}

## Overview

{2-3 paragraph synthesis of everything the wiki knows about this entity, drawn from all sources}

## Key facts

- {Important factual details, aggregated across sources}

## Mentioned in

- [[source - {title}]] — {what that source says about this entity}

## Related

- [[{other entities or concepts this connects to}]]

## Open questions

- {Things we don't know yet, or would benefit from more sources}
```

### Concept pages (`wiki/concepts/`)

Pages about ideas, topics, methods, theories, debates. File name format: `{Concept Name}.md`. These synthesize understanding across sources.

Template:
```
---
type: concept
source_count: {number of sources informing this page}
last_updated: YYYY-MM-DD
tags: []
---

# {Concept Name}

{One-line definition or summary}

## Overview

{Multi-paragraph synthesis of the concept as understood across all sources. This is the evolving "state of knowledge."}

## Key perspectives

{Different viewpoints, approaches, or schools of thought — especially if sources disagree}

## Evidence and data

{Specific data points, statistics, or findings from sources that bear on this concept}

## Contradictions and debates

{Where sources disagree, where the evidence is mixed, where more information is needed}

## Sources

- [[source - {title}]] — {what this source contributes to understanding of the concept}

## Related

- [[{other concepts, entities}]]
```

### Output pages (`wiki/outputs/`)

Pages generated from queries — comparisons, analyses, syntheses, tables. File name format: descriptive, e.g. `comparison - DAC methods by cost.md`.

Template:
```
---
type: output
query: "{the question that generated this page}"
date_created: YYYY-MM-DD
sources_used: []
tags: []
---

# {Descriptive title}

{The analysis, comparison, or synthesis. Format varies by content — could be prose, a table, a structured comparison, etc.}

## Sources consulted

- [[{pages used to generate this output}]]
```

## Operations

### Ingest

Triggered when the human says to process a new source in `raw/`.

Workflow:
1. Read the full source document.
2. Discuss key takeaways with the human — what's interesting, what's surprising, what connects to existing knowledge.
3. Create a source summary page in `wiki/sources/`.
4. For each entity mentioned: check if an entity page exists. If yes, update it with new information from this source. If no, create one.
5. For each concept touched: check if a concept page exists. If yes, update it — integrate new perspectives, note contradictions, add data points. If no, create one.
6. Update `wiki/index.md` — add entries for any new pages, update summaries for modified pages.
7. Append to `wiki/log.md`.
8. Report to the human: what pages were created, what was updated, any contradictions found, any suggested follow-ups.

Important:
- When updating existing pages, ADD information — don't delete or overwrite unless the new source definitively supersedes old claims. Note contradictions explicitly.
- Always use `[[wikilinks]]` when referencing other wiki pages.
- Be generous with cross-references. If a concept page mentions an entity, link it. If two concepts are related, link them. The link density is what makes the wiki valuable.

### Query

Triggered when the human asks a question.

Workflow:
1. Read `wiki/index.md` to identify relevant pages.
2. Read those pages.
3. Synthesize an answer with citations to wiki pages (using `[[wikilinks]]`).
4. If the answer is substantial and reusable (a comparison, an analysis, a synthesis), offer to save it as an output page in `wiki/outputs/`. If the human agrees, create the page, update the index, and log it.
5. If the question reveals a gap — important information the wiki doesn't have — say so honestly rather than generating a weak answer. Suggest what sources to look for.

### Lint

Triggered when the human asks for a health check, or proactively when you notice issues.

Checks to perform:
- **Orphan pages**: wiki pages with no inbound links from other pages. These should be linked from somewhere.
- **Dead links**: `[[wikilinks]]` pointing to pages that don't exist. Either create the page or remove the link.
- **Stale content**: claims on concept/entity pages that have been superseded by newer sources. Update them.
- **Missing pages**: important entities or concepts mentioned across multiple sources but lacking their own dedicated page. Create them.
- **Thin pages**: pages with very little content that could be enriched from existing sources.
- **Contradictions**: unresolved conflicts between sources that haven't been noted on the relevant pages.
- **Index accuracy**: ensure `wiki/index.md` matches the actual contents of the wiki.

After a lint pass, update the log with what was found and fixed.

## Conventions

### Writing style
- Clear, concise, factual prose. Not academic, not casual — like a well-written Wikipedia article.
- Use bullet points for lists of facts. Use prose for synthesis and analysis.
- Always attribute claims to their sources using `[[wikilinks]]`.
- Note uncertainty. If something is claimed by only one source, say so. If sources disagree, present both sides.

### Wikilinks
- Use `[[Page Name]]` format for all cross-references.
- Link generously. When you mention an entity or concept that has a wiki page, link it.
- Don't create links for trivial references (common words, generic concepts that don't warrant their own page).

### Frontmatter
- Every wiki page gets YAML frontmatter with at minimum: `type`, `last_updated` (or `date_ingested` for sources), and `tags`.
- Tags should be lowercase, hyphenated (e.g. `climate-tech`, `machine-learning`).
- Keep `source_count` accurate on entity and concept pages — it helps prioritize which pages are well-supported vs. thinly sourced.

### File naming
- Source pages: `source - {descriptive title}.md`
- Entity pages: `{Entity Name}.md` (title case)
- Concept pages: `{Concept Name}.md` (title case)
- Output pages: descriptive, lowercase with hyphens or title case — be consistent.

### Log format
Every log entry uses this format so it's grep-parseable:
```
## [YYYY-MM-DD] {operation} | {brief title}

{Details of what happened}
```

Operations are: `ingest`, `query`, `lint`, `update`, `create`.

## Tips for yourself

- When starting a new session, read `wiki/log.md` (at least the last 10 entries) and `wiki/index.md` to orient yourself.
- When the wiki grows large, use grep/search to find relevant pages rather than reading the entire index.
- If the human asks a question and the wiki doesn't have enough information to answer well, say so honestly rather than generating a weak answer. Suggest what sources to look for.
- Periodically suggest a lint pass to the human — don't wait to be asked.
- If you notice the schema (this file) could be improved based on how the wiki is evolving, suggest changes to the human.

