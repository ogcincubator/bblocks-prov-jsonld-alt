# Alternative representations of the W3C PROV model

Testing of alternative representations and transforms for the W3C PROV model

Provenance defined using the [W3C PROV model](https://www.w3.org/TR/prov-overview/) is a DAG (non-cyclic graph)
based on three main object types: Entity, Activity and Agent.

The candidate "canonical" PROV repository (https://ogcincubator.github.io/bblocks-prov-schema )
defines a JSON schema and matching JSON-LD context using the [OGC Building Blocks](https://ogcincubator.github.io/bblocks-docs/) methodology,
for the W3C PROV model, using the canonical terminology used in the PROV ontology as element names.

Since the development of this schema, W3C PROV itself defines multiple concrete syntaxes for the
same underlying model - PROV-N, PROV-XML, PROV-JSON, PROV-O/RDF, and the non-normative member
submission [PROV-JSONLD](https://www.w3.org/submissions/prov-jsonld/) - each with different
tradeoffs for readability, tooling, and linked-data integration.

## Design Principles

  - **Lightweight** A serialization MUST support lightweight Web applications.
  - **Natural** A serialization MUST look natural to its targeted community of users.
  - **Semantic** A serialization MUST allow for semantic markup and integration with linked data applications.
  - **Efficient** A serialization MUST be efficiently processable.

This repository is designed to document and explore the potential for reconciliation of
these models across multiple profile representations of the PROV concepts.

## How this repository is organized: profiles of a common PROV base

Every concrete PROV representation defined here (W3C PROV-N, PROV-XML, PROV-JSON, PROV-O/RDF,
PROV-JSONLD) is declared as a **profile** (`isProfileOf`) of a single shared anchor block,
`ogc.ogc-utils.prov.w3c-prov-base` ("W3C PROV Representation Base") - the same relationship as the W3C
[Profiles Vocabulary (PROF)](https://www.w3.org/TR/dx-prof/)'s `prof:isProfileOf`: each one is a
concrete, backward-compatible specialization of the same underlying PROV-DM concepts
(`Entity`, `Activity`, `Agent` and their relations), differing only in concrete syntax.

A separate, pre-existing register imported here, `ogc.ogc-utils.prov` ("OGC PROV Chain", from
[`bblock-prov-schema`](https://ogcincubator.github.io/bblock-prov-schema/)), models the same
underlying PROV-O concepts again, structured as JSON Schema rather than a `@context`/`@graph`
linked-data document. **It is also a profile of the same PROV-O base** - not a fundamentally
different model, just another concrete syntax - and is treated as such throughout this
repository: `ogc.ogc-utils.prov.w3c-prov-jsonld` declares `isProfileOf` it directly (alongside
the shared `ogc.ogc-utils.prov.w3c-prov-base` anchor), and the transforms in
`ogc.ogc-utils.prov.ogc-prov-chain-forms` / `ogc.ogc-utils.prov.w3c-prov-jsonld` convert
losslessly between W3C PROV-JSONLD and OGC PROV Chain precisely because both are just different
concrete syntaxes for the same PROV-O statements. That it is a pre-existing, separately
maintained register we don't own only means it cannot itself declare `isProfileOf` back towards
this repository's blocks - it does not change the nature of the relationship. See the
`ogc.ogc-utils.prov.w3c-prov-base` block's own documentation for how the two relate, and the
blocks above for the transforms that prove and implement that relationship.


## Building Blocks

### `ogc.ogc-utils.prov.ogc-prov-chain-forms` — OGC PROV Chain: Array ⇄ Object Conversion

**Type:** model

Two transforms that convert an OGC PROV Chain document (from the bblock-prov-schema register) between its two allowed shapes: a flat top-level array (every record referencing others by full-IRI id) and a nested single object (one root record with related records inlined). Both shapes validate against the same imported schema. Purely internal to OGC PROV Chain - no W3C PROV representation is involved here; see the W3C PROV-JSONLD block for the transforms that bridge to/from W3C PROV-JSONLD.

### `ogc.ogc-utils.prov.w3c-prov-base` — W3C PROV Representation Base

**Type:** model

Cross-reference anchor for the W3C PROV data model (PROV-DM), shared by every concrete PROV serialization/representation profile (W3C PROV-N, PROV-XML, PROV-JSON, PROV-O/RDF, PROV-JSONLD). This block carries no concrete syntax of its own; each representation-specific sibling block declares itself a profile of this one and supplies its own schema/context/examples. It directly cross-references the canonical OGC PROV Chain schema blocks for the same PROV-DM concepts, and documents how those can be used as an extension point substitution target for anyone wanting a specialized OGC PROV Chain profile. See the full description for details.

### `ogc.ogc-utils.prov.w3c-prov-json` — W3C PROV-JSON

**Type:** schema

The PROV-JSON serialization: a non-normative, flat, statement-oriented JSON encoding of the W3C PROV data model (W3C Member Submission). A profile of the W3C PROV Representation Base.

### `ogc.ogc-utils.prov.w3c-prov-jsonld` — W3C PROV-JSONLD

**Type:** schema

The PROV-JSONLD serialization: a non-normative, linked-data JSON-LD encoding of the W3C PROV data model (W3C Member Submission), using context and graph blocks rather than the flat statement-keyed layout of PROV-JSON. A profile of the W3C PROV Representation Base.

### `ogc.ogc-utils.prov.w3c-prov-n` — W3C PROV-N

**Type:** model

The PROV Notation (PROV-N): a human-readable, non-XML/non-JSON textual notation for the W3C PROV data model, primarily used in specifications and diagnostics. A profile of the W3C PROV Representation Base.

### `ogc.ogc-utils.prov.w3c-prov-rdf` — W3C PROV-O / RDF

**Type:** model

The RDF binding of the W3C PROV data model via the PROV Ontology (PROV-O), serializable as Turtle, N-Triples, RDF/XML, N-Quads, TriG, etc. A profile of the W3C PROV Representation Base.

### `ogc.ogc-utils.prov.w3c-prov-xml` — W3C PROV-XML

**Type:** model

The PROV-XML serialization: an XML Schema binding of the W3C PROV data model. A profile of the W3C PROV Representation Base.

