# PROV Representation Base

This block is a **cross-reference anchor**, not a concrete syntax. It exists so that every
concrete PROV serialization/representation defined in this repository can declare a common
ancestor via `isProfileOf`, instead of each one being an unrelated island:

- [PROV-N](bblocks://ogc.ogc-utils.prov.prov-n) — the human-readable notation
- [PROV-XML](bblocks://ogc.ogc-utils.prov.prov-xml) — the XML schema-based serialization
- [PROV-JSON](bblocks://ogc.ogc-utils.prov.prov-json) — the (non-normative, W3C member submission) JSON serialization
- [PROV-O/RDF](bblocks://ogc.ogc-utils.prov.prov-rdf) — the RDF/OWL ontology binding (Turtle, N-Triples, RDF/XML, ...)
- [PROV-JSONLD](bblocks://ogc.ogc-utils.prov.prov-jsonld) — the (non-normative, W3C member submission) JSON-LD serialization

Each of these is declared `isProfileOf` this block: same underlying PROV-DM record types and
relations (`Entity`, `Activity`, `Agent`, `wasGeneratedBy`, `used`, `wasAssociatedWith`, ...),
different concrete syntax.

A distinct, separately maintained representation of the PROV-DM model — the ["Provenance Chain"
JSON schema](bblocks://ogc.ogc-utils.prov) from
[`bblock-prov-schema`](https://ogcincubator.github.io/bblock-prov-schema/) — predates this
repository and is referenced here (`seeAlso`) rather than duplicated. It models the same
underlying concepts but as a nested/inline JSON object graph, rather than a flat statement list
like PROV-JSON/PROV-JSONLD. See the [PROV-JSONLD block](bblocks://ogc.ogc-utils.prov.prov-jsonld)
for a transform between it and the PROV-JSONLD context/graph representation.

## Why a base block instead of a shared schema

None of the PROV representations share a common JSON Schema — PROV-N and PROV-XML aren't JSON at
all, and PROV-JSON/PROV-JSONLD structure the same statements very differently (nested-object-graph
vs. flat array-of-statements-with-`@context`/`@graph`). What *is* shared is the underlying data
model (PROV-DM) and its RDF binding (PROV-O), which this block references directly via `ontology`
and `concept` rather than re-declaring.
