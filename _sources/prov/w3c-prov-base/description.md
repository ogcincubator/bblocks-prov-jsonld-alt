# W3C PROV Representation Base

This block is a **cross-reference anchor**, not a concrete syntax. It exists so that every
concrete **W3C PROV** serialization/representation defined in this repository can declare a
common ancestor via `isProfileOf` - the same relationship as the W3C
[Profiles Vocabulary (PROF)](https://www.w3.org/TR/dx-prof/)'s `prof:isProfileOf`: each profile
below is a concrete, backward-compatible specialization of the same underlying PROV-DM concepts
(`Entity`, `Activity`, `Agent` and their relations), differing only in concrete syntax, instead of
being unrelated islands.

## The W3C PROV representation profiles

All five are declared `isProfileOf` this block, and cross-link one another (`seeAlso`) as
alternative representations of the same underlying model:

| Profile | Syntax | Normative status | What distinguishes it |
|---|---|---|---|
| [`W3C PROV-N`](bblocks://ogc.ogc-utils.prov.w3c-prov-n) | Custom textual notation | W3C Recommendation | Human-readable notation for specs/diagnostics; not XML or JSON |
| [`W3C PROV-XML`](bblocks://ogc.ogc-utils.prov.w3c-prov-xml) | XML (XSD-defined) | W3C Note | XML Schema binding of PROV-DM |
| [`W3C PROV-JSON`](bblocks://ogc.ogc-utils.prov.w3c-prov-json) | JSON, flat statement-keyed (never nests one record inside another) | Non-normative (W3C Member Submission) | Predates PROV-JSONLD; flat but not linked-data |
| [`W3C PROV-O / RDF`](bblocks://ogc.ogc-utils.prov.w3c-prov-rdf) | RDF (Turtle, N-Triples, RDF/XML, N-Quads, TriG, ...) | W3C Recommendation (PROV-O) | Full ontology binding; any RDF serialization applies |
| [`W3C PROV-JSONLD`](bblocks://ogc.ogc-utils.prov.w3c-prov-jsonld) | JSON-LD (context/graph blocks) | Non-normative (W3C Member Submission) | Linked-data JSON; flat graph array of typed records |

## Cross-references to the OGC PROV Chain schema blocks

> **Not to be confused:** despite both being "PROV JSON", **W3C PROV-JSON**
> ([`ogc.ogc-utils.prov.w3c-prov-json`](bblocks://ogc.ogc-utils.prov.w3c-prov-json)) and
> **OGC PROV Chain**'s JSON representation
> ([`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov), cross-referenced below) use fundamentally
> different shapes - the former groups records by type and never nests one record inside another,
> the latter supports embedding related records inline in its single-object form. See
> [`ogc.ogc-utils.prov.w3c-prov-json`](bblocks://ogc.ogc-utils.prov.w3c-prov-json)'s description
> for a detailed side-by-side comparison and the JSON Schema that enforces it.

A separately maintained representation of the same PROV-O concepts - the **OGC PROV Chain** JSON
Schema family from [`bblock-prov-schema`](https://ogcincubator.github.io/bblock-prov-schema/) -
predates this repository and is reused here directly (`dependsOn`) rather than duplicated. It is,
in effect, **also a profile** of the same underlying PROV-O base as the five above: just JSON
Schema-structured (nested object graph, or flat array of full-IRI-referencing records) rather than
a context/graph linked-data document. The transforms declared in
[`ogc.ogc-utils.prov.w3c-prov-jsonld`](bblocks://ogc.ogc-utils.prov.w3c-prov-jsonld) losslessly
convert between it and W3C PROV-JSONLD precisely *because* both describe the same PROV-O
statements - that interoperability is the practical proof of the profile relationship, which is
now declared formally: [`ogc.ogc-utils.prov.w3c-prov-jsonld`](bblocks://ogc.ogc-utils.prov.w3c-prov-jsonld)
lists [`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov) in its own `isProfileOf`, alongside this
base block. The OGC PROV Chain register cannot reciprocate that declaration (it is a pre-existing
register we don't own, so we can't add metadata to it), but that is an ownership limitation, not
evidence the relationship is one-sided or conceptually different:

| Block | Role |
|---|---|
| [`Provenance Chain`](bblocks://ogc.ogc-utils.prov) | Top-level schema; accepts either a flat array of records or a single nested object |
| [`Single Schema for PROV`](bblocks://ogc.ogc-utils.prov-bundled) | The original, pre-split single-schema PROV mix-in |
| [`Prov Entity`](bblocks://ogc.ogc-utils.prov-entity) | Sub-schema for `Entity` records |
| [`Prov Activity`](bblocks://ogc.ogc-utils.prov-activity) | Sub-schema for `Activity` records |
| [`Prov Agent`](bblocks://ogc.ogc-utils.prov-agent) | Sub-schema for `Agent` records |

These model the same underlying concepts as the W3C representations above, but as JSON Schema:
either a nested/inline JSON object graph, or a flat array of full-IRI-referencing records - rather
than a flat statement list keyed by a graph array like PROV-JSON/PROV-JSONLD. See:

- [`ogc.ogc-utils.prov.w3c-prov-jsonld`](bblocks://ogc.ogc-utils.prov.w3c-prov-jsonld)'s
  [Transforms tab](https://ogcincubator.github.io/bblocks-docs/create/transforms) for the
  conversions between W3C PROV-JSONLD and the OGC PROV Chain array form;
- [`ogc.ogc-utils.prov.ogc-prov-chain-forms`](bblocks://ogc.ogc-utils.prov.ogc-prov-chain-forms)'s
  Transforms tab for the conversions between OGC PROV Chain's own array and single-object forms.

## How everything interconnects

All five W3C PROV representations below are mutually interchangeable via `prov`-library
transforms, declared as each format's own
[Transforms](https://ogcincubator.github.io/bblocks-docs/create/transforms). The table reads as
"row → column": a ✅ means a direct transform exists from the row format to the column format.

| from \ to | PROV-XML | PROV-JSON | PROV-O/RDF | PROV-JSONLD | PROV-N |
|---|:---:|:---:|:---:|:---:|:---:|
| **PROV-XML** | - | ✅ | ✅ | ✅ | ✅ |
| **PROV-JSON** | ✅ | - | ✅ | ✅ | ✅ |
| **PROV-O/RDF** | ✅ | ✅ | - | ✅ | ✅ |
| **PROV-JSONLD** | ✅ | ✅ | ✅ | - | ✅ |
| **PROV-N** | - | - | - | - | - |

PROV-N is a transform *target only*: the `prov` library has no PROV-N parser, so nothing
converts *from* PROV-N to any other format. All other pairs above are fully bidirectional,
converting directly - none of them need to hop through PROV-JSONLD (or any other format) as an
intermediate.

PROV-JSONLD additionally connects one level further, to the separately maintained **OGC PROV
Chain** JSON representation ([`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov), see the
previous section):

| Step | Direction | Declared in |
|---|---|---|
| 1 | PROV-JSONLD ↔ OGC PROV Chain, **array** form | [`ogc.ogc-utils.prov.w3c-prov-jsonld`](bblocks://ogc.ogc-utils.prov.w3c-prov-jsonld) |
| 2 | OGC PROV Chain **array** form ↔ **object** form | [`ogc.ogc-utils.prov.ogc-prov-chain-forms`](bblocks://ogc.ogc-utils.prov.ogc-prov-chain-forms) |

This path is exclusively via PROV-JSONLD because the `prov` library's OGC PROV Chain support is
implemented against its native PROV-JSONLD model, not against PROV-XML/JSON/RDF directly. See
each format block's own Transforms tab for the full, current list of transforms.

## Extension points vs. `isProfileOf`: how the interconnection graph is actually built

The viewer's block-relationship graph for the five W3C PROV representations above is built from
their `isProfileOf` declarations (all pointing here), rendered as blue edges, plus a redundant
`dependsOn` pointing at the same target (a workaround for a viewer display limitation: at the time
of writing, the viewer only draws a block's dependency graph when it has a `dependsOn` entry, so a
block declaring `isProfileOf` alone renders no graph at all even though the graph-drawing code
itself does understand `isProfileOf` edges once that check is passed) - **not** from the
`extensionPoints` mechanism. `extensionPoints` substitutes a `$ref`'d sub-schema inside a *JSON
Schema*-backed block; PROV-N, PROV-XML and PROV-O/RDF aren't JSON at all, and PROV-JSON/PROV-JSONLD
don't structure records as composable `$ref`s either, so there's no schema fragment to substitute.
`isProfileOf` (declaring "this is the same underlying model, differently encoded") plus
documented, working transforms (the practical, testable proof of that relationship) is the
correct/only applicable mechanism for these five blocks. `extensionPoints` *does* apply below, one
level down, to the JSON-Schema-backed OGC PROV Chain sub-schemas.

## Using this as an extension point

This block itself has no JSON Schema (see below for why), so it cannot declare `extensionPoints`
directly. But since it cross-references [`ogc.ogc-utils.prov-entity`](bblocks://ogc.ogc-utils.prov-entity),
[`ogc.ogc-utils.prov-activity`](bblocks://ogc.ogc-utils.prov-activity) and
[`ogc.ogc-utils.prov-agent`](bblocks://ogc.ogc-utils.prov-agent) - the exact sub-schemas that
[`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov) references internally - anyone wanting a
*specialized* OGC PROV Chain profile (e.g. an `Entity` constrained to a specific application
schema) can use the
[extension points mechanism](https://ogcincubator.github.io/bblocks-docs/create/extension-points)
to substitute them, without having to replicate the whole "Provenance Chain" schema structure:

```json
{
  "name": "My Specialized Provenance Chain",
  "extensionPoints": {
    "baseBuildingBlock": "bblocks://ogc.ogc-utils.prov",
    "extensions": {
      "bblocks://ogc.ogc-utils.prov-entity": "bblocks://myorg.myproject.my-entity"
    }
  }
}
```

This block is the documented, discoverable anchor for that substitution pattern - the identifiers
in the table above are exactly what to plug into `extensionPoints.extensions`.

## Why a base block instead of a shared schema

None of the W3C PROV representations share a common JSON Schema - PROV-N and PROV-XML aren't JSON
at all, and PROV-JSON/PROV-JSONLD structure the same statements very differently
(nested-object-graph vs. flat array-of-statements-with-`@context`/`@graph`). What *is* shared is
the underlying data model (PROV-DM) and its RDF binding (PROV-O), which this block references
directly via `ontology` and `concept` rather than re-declaring, plus the OGC PROV Chain schema
blocks cross-referenced above for anyone who does want a JSON Schema to extend.
