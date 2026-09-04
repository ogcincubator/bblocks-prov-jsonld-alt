# OGC Provenance option for JSON

Repo for testing alternative approaches for encoding the PROV model in JSON.

There is a pre-JSON schema legacy, and a more recent proposal (SOTON) for a JSON-LD native schema (using JSON-LD keywords), with specific encoding options enforced by JSON schema (JSON-LD has many isomorphic forms)

## (Claude) analysis of the options

❯` Compare the prov-soton approach to provenance, grounded in JSON-LD syntax and compare to the design of the bblocks-prov-schema building blocks to provide a rationale for choosing one or the other. Consider the possibility of the prov:Bundle concept allowing known alternative schemas to allow the uplift of heterogenous json schemas into a common valid PROV RDF graph using JSON-LD.`

### Edited response: (trimmed and emphases added)

bblocks-prov-schema deliberately rejects that shape. The README states why explicitly: the W3C draft serialisations:
1. don't cleanly JSON-LD-map to PROV-O, 
2. are JSON-LD-specific and break plain JSON Schema validation,
3. were never formally published as JSON Schema, and 
4. force a bespoke "register everything under an entities property" structure instead of letting an existing object just be a prov:Entity. 
5. 
6. Instead it builds prov/prov-entity/prov-activity/prov-agent as **composable mix-ins**: $anchor/$ref fragments other building blocks (a GeoJSON Feature, a STAC Item, anything) can pull in via bblocks://…, with *WithRequirements variants that just require some PROV signal (provType, wasGeneratedBy, …) rather than a container wrapper. It supports both id-linked graphs and inline nesting in the same schema (see example-withrefs.json, example-llm.json), so PROV **becomes a trait an object carries, not a document format it must be siloed into.** Notably its context.jsonld is nearly identical term-for-term to soton's — both uplift to essentially the same PROV-O triples; the divergence is entirely in document shape and composability, not ontology coverage.


### Rationale

For the stated goal of this project — annotating arbitrary OGC resources (Features, STAC Items, API payloads) with provenance without forcing them into a separate document shape — bblocks-prov-schema's mix-in design is the right default. Reified relation-nodes (soton's real advantage: an Association/Usage/Generation node can freely carry its own qualifiers) are still reachable in the bblocks schema via Influence/qualified*, just opt-in rather than the default shape.

prov:Bundle for heterogeneous uplift — good idea, not yet built either place

I checked: neither bblock currently uses prov:Bundle as an active mechanism — it only appears as a legal @type value inheriting Entity (prov-entity/schema.json). But the idea holds up structurally:

- prov:Bundle is PROV's named-provenance-subgraph concept — a Bundle is itself an Entity, so it can carry its own provenance (who asserted it, from what source schema, via what uplift process), and prov:mentionOf/asInBundle let the same real-world entity be described differently across bundles without collision.
- JSON-LD's named-graph form ({"@id": "urn:...", "@graph": [...]}) maps directly onto this. Soton's Document wrapper is already Bundle-shaped, just unnamed — tag it "@type": "prov:Bundle" with an @id and each heterogeneous source's uplifted output becomes an independently identified named graph.
- That gives a real strategy: run each source schema's own context over its native payload, wrap each uplift as a named prov:Bundle, union them via top-level @graph. Cross-source identity gets reconciled explicitly (mentionOf/sameAs) instead of silently merging on blank nodes. bblocks mix-in objects are what populate a bundle's contents once you're uplifting a whole document; the soton statement-graph style is a natural fit for authoring a bundle's contents when a source system emits provenance as a batch of events.
- Caveat: bundled content sits outside the default graph in PROV-O semantics, and this repo's SHACL/JSON-Schema test harness currently validates a flat default graph (see the .ttl/_report.json outputs) — adopting Bundle for multi-source merge would need explicit extension of that validation pipeline, not just a context change.

So: keep the mix-in schema as the primary annotation mechanism; introduce prov:Bundle only as an additional opt-in layer specifically for merging multiple independently-uplifted heterogeneous sources into one graph — that's the exact problem it was designed for, and it's currently unclaimed territory in both bblocks.