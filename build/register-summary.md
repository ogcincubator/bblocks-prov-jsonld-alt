# Alternative JSON schemas for W3C PROV model

Testing of alternative JSON schemas for PROV

Provenance defined using the [W3C PROV-O model](https://www.w3.org/TR/prov-o/) is a DAG (non-cyclic graph) based on three main object types: Entity, Activity and Agent.

The candidate "canonical" PROV repository (https://ogcincubator.github.io/bblocks-prov-schema ) defines a JSON schema and matching JSON-LD context using the [OGC Building Blocks](https://ogcincubator.github.io/bblocks-docs/) methodology, 
for W3C PROV-O model, using the canonical terminology used in the PROV ontology as element names.

Note that the PROV working group originally defined a number of JSON serialisation options, however these have limited uptake and do no allow PROV-O to annotate other schemas. This implementation uses modern JSON schema and JSON-LD mechanisms to provide a complete mapping from JSON to PROV-O model.

Since the development of this schema another proposal has been submitted as a W3C member submission: 
[https://www.w3.org/submissions/prov-jsonld/](https://www.w3.org/submissions/prov-jsonld/)

A common thread is the stated rationale:

"The rationale for this is consistent with the design principles:

" the family of PROV specifications lacks a serialization capable of simultaneously addressing all of the following requirements:

  - **Lightweight** A serialization MUST support lightweight Web applications.
  - **Natural** A serialization MUST look natural to its targeted community of users.
  - **Semantic** A serialization MUST allow for semantic markup and integration with linked data applications.
  - **Efficient** A serialization MUST be efficiently processable.
In our view, none of the existing PROV serializations supports all these requirements simultaneously."

This repository is designed to document and explore the potential for reconciliation of these models.


## Building Blocks

### `ogc.ogc-utils.prov-soton` — 2024 w3c

**Type:** schema

A BBlock to cross check examples across the University of The PROV-JSONLD Serialization w3c member submission

