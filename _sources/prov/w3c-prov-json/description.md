# W3C PROV-JSON

PROV-JSON is a non-normative W3C Member Submission (not a Recommendation) predating PROV-JSONLD.
It has no *official* published JSON Schema — the format is described only in prose in the
submission — so this block references the specification directly (`sources`) and additionally
supplies its own JSON Schema, written to capture that prose as an enforceable structural
constraint (see below), rather than treating a third-party schema as normative. It is the flat,
statement-keyed sibling of [`ogc.ogc-utils.prov.w3c-prov-jsonld`](bblocks://ogc.ogc-utils.prov.w3c-prov-jsonld)
(W3C PROV-JSONLD): both group records by relation type, but PROV-JSON has no context/graph blocks
and is not linked data.

## W3C PROV-JSON vs. OGC PROV JSON ([`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov)) - not the same shape

Both are JSON encodings of the same underlying PROV-DM concepts, but they structure records
completely differently - **this is not a case of one being "the JSON form" of the other**:

| | W3C PROV-JSON (this block) | OGC PROV Chain ([`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov)) |
|---|---|---|
| Top-level grouping | By **record/relation type** (`entity`, `activity`, `wasGeneratedBy`, ...) | By **individual record**, each self-describing via its own `provType` field |
| Shape | Object of objects: `{"entity": {"id1": {...}, "id2": {...}}, ...}` | Either a flat **array** of `{id, provType, ...}` records, or a single **nested object** embedding related records inline |
| Cross-references between records | Always a bare identifier (string, or array of strings) | Array form: bare identifier (like PROV-JSON). Object form: the related record is **embedded inline**, not referenced |
| Nesting one record inside another | **Never** (only `bundle` nests, and that's a distinct PROV concept - a sub-graph, not a record) | **Yes**, in its object form - that's the whole point of that form |

This block's [JSON Schema](https://ogcincubator.github.io/bblocks-docs/create/schema) enforces the
"never nests a record inside another" rule structurally: every attribute value must be a literal,
a PROV-JSON typed-value wrapper (`{"$": ..., "type": ...}`), or an array of these - never an object
embedding a full nested record. Feeding this block's schema a document using OGC PROV Chain's
nested-object style (e.g. `"wasGeneratedBy": {"id": "...", "provType": "Activity", ...}` instead of
`"wasGeneratedBy": {"_:id1": {"prov:activity": "..."}}`) fails validation - that's precisely the
distinction this schema exists to catch.

This block's [Transforms](https://ogcincubator.github.io/bblocks-docs/create/transforms) to and
from W3C PROV-JSONLD and the other W3C PROV representations always produce/consume this
never-nested shape, since they go through the `prov` library's own native PROV-JSON
parser/serializer rather than any hand-written conversion logic.

