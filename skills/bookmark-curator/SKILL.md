---
name: bookmark-curator
description: Audit, migrate, deduplicate, organize, and maintain bookmark libraries across a browser and Raindrop.io. Use for bookmark cleanup, Safari-to-Raindrop migration, collection or tag design, stale-link review, and recurring bookmark hygiene. Start read-only and require approval before creating, moving, retagging, or deleting bookmarks.
---

# Bookmark Curator

Build a small, useful retrieval system rather than reproducing a browser folder tree in Raindrop.

## Start with evidence

Inventory each source read-only before proposing changes:

- total items, folders or collections, tags, favorites, and content types;
- exact and normalized URL overlap between sources;
- dominant domains and a representative random sample;
- local/private URLs, authenticated dashboards, bookmarklets, and session-specific URLs;
- duplicates, broken links, empty or low-value collections, and untagged items.

For Safari, use `scripts/safari_bookmark_inventory.py` when the bookmark plist is locally readable. Treat Reading List separately from ordinary bookmarks. For Raindrop, prefer its MCP read-only tools such as `fetch_current_user`, `find_collections`, `find_tags`, `fetch_popular_keywords`, and sampled `find_bookmarks` calls.

Do not infer that a link is safe to delete merely because it is old, broken, duplicated across systems, or returned by semantic cleanup tools.

## Separate the jobs of each system

Keep browser bookmarks as a compact launchpad for destinations the user repeatedly opens: local services, authenticated portals, dashboards, web apps, bookmarklets, and a small number of habitual sites.

Use Raindrop as the durable library for things the user may want to retrieve, read, compare, cite, or reuse: articles, guides, documentation, tools worth remembering, repositories, media, and references.

When a URL belongs in both roles, duplication is acceptable. Do not remove a browser launchpad link just because it exists in Raindrop.

## Keep the taxonomy small

Use collections for broad workflow or object type and tags for cross-cutting topics. Prefer Raindrop's Unsorted collection as the inbox instead of creating another inbox.

Start with roughly four to six durable collections. Common useful shapes are:

- Read Later
- Reference
- Tools
- Media, only when volume justifies it
- Archive, only when the user wants retained but inactive material separated

Start with at most eight to twelve topic tags based on actual repeated retrieval needs. Add a tag only when it will group several items or answer a likely future search. Avoid tags that merely repeat a domain, collection, content type, or words already obvious in the title. Avoid nested topic taxonomies until usage proves they are needed.

## Plan before mutation

Produce a staged plan with counts and explicit decision rules:

1. Back up or export the browser bookmarks.
2. Canonicalize URLs and exclude items already present in Raindrop.
3. Establish the minimal collections and controlled tag vocabulary.
4. Migrate only missing, high-confidence Raindrop candidates in small batches.
5. Verify created bookmark count, URLs, and collection placement before changing the browser source.
6. Curate the existing Raindrop library in bounded batches.
7. Put deletion candidates into a review queue with a reason; after approval, use recoverable Trash deletion first.

Do not perform mutations during an audit or planning request. Before the first write in a cleanup session, show the proposed batch and obtain explicit approval. Keep deletion batches at 25 items or fewer unless the user approves a larger, clearly enumerated rule-based batch.

## Triage rules

Use these outcomes:

- **Browser launchpad** — frequent destination, local service, account portal, dashboard, web app, or bookmarklet.
- **Raindrop / Read Later** — content the user intends to consume once.
- **Raindrop / Reference** — durable knowledge likely to be searched or reused.
- **Raindrop / Tools** — a tool, repository, service, calculator, or resource worth remembering but not necessarily launched frequently.
- **Review for deletion** — expired signed/session URL, obsolete one-off workflow, superseded copy, inaccessible low-value page, accidental save, or content with no plausible future use.
- **Needs user judgment** — personal, financial, employment, academic, or ambiguous links whose value cannot be inferred safely.

Semantic misplaced/mistagged results are candidates, not verdicts. Verify title, URL, notes, collection, tags, and when needed page content before changing them.

## Recurring maintenance

Default recurring runs to read-only reporting. Report new inbox volume, untagged count, likely duplicates, broken or transient URLs, taxonomy drift, and a small proposed action batch. Stay quiet when there is no meaningful change if the run is automated.

Suggested cadence:

- weekly: process recent Unsorted items and new browser reading-list candidates;
- monthly: review stale/transient links, low-use tags, misplaced items, and collection balance;
- quarterly: reconsider the taxonomy itself, merging or removing structures that are not earning their keep.

Never create a new collection or tag during recurring maintenance merely to classify one item. Never delete automatically unless the user has supplied an explicit, narrow deletion rule for that run.
