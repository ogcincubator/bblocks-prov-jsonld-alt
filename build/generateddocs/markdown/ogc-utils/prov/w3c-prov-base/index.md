
# W3C PROV Representation Base (Model)

`ogc.ogc-utils.prov.w3c-prov-base` *v0.1*

Cross-reference anchor for the W3C PROV data model (PROV-DM), shared by every concrete PROV serialization/representation profile (W3C PROV-N, PROV-XML, PROV-JSON, PROV-O/RDF, PROV-JSONLD). This block carries no concrete syntax of its own; each representation-specific sibling block declares `isProfileOf` this one and supplies its own schema/context/examples. It directly cross-references the canonical OGC PROV Chain schema blocks for the same PROV-DM concepts (`dependsOn`), and documents how those can be used as an `extensionPoints` substitution target for anyone wanting a specialized OGC PROV Chain profile.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

# W3C PROV Representation Base

This block is a **cross-reference anchor**, not a concrete syntax. It exists so that every
concrete **W3C PROV** serialization/representation defined in this repository can declare a
common ancestor via `isProfileOf` - the same relationship as the W3C
[Profiles Vocabulary (PROF)](https://www.w3.org/TR/dx-prof/)'s `prof:isProfileOf`: each profile
below is a concrete, backward-compatible specialization of the same underlying PROV-DM concepts
(`Entity`, `Activity`, `Agent` and their relations), differing only in concrete syntax, instead of
being unrelated islands.

> **Note on links below:** identifiers are given in `code` form (e.g. `ogc.ogc-utils.prov.w3c-prov-n`)
> rather than as clickable Markdown links. The `bblocks://` URI scheme used elsewhere in this
> repository (e.g. in `bblock.json` metadata) is resolved by the Building Blocks tooling and
> viewer for structured fields, but is not a real browser-navigable URL scheme - writing it as a
> plain link target in prose produces a dead link once rendered. Look up any identifier below in
> this register's block list to open its page.

## The W3C PROV representation profiles

All five are declared `isProfileOf` this block:

| Profile | Identifier | Syntax | Normative status | What distinguishes it |
|---|---|---|---|---|
| W3C PROV-N | `ogc.ogc-utils.prov.w3c-prov-n` | Custom textual notation | W3C Recommendation | Human-readable notation for specs/diagnostics; not XML or JSON |
| W3C PROV-XML | `ogc.ogc-utils.prov.w3c-prov-xml` | XML (XSD-defined) | W3C Note | XML Schema binding of PROV-DM |
| W3C PROV-JSON | `ogc.ogc-utils.prov.w3c-prov-json` | JSON, flat statement-keyed | Non-normative (W3C Member Submission) | Predates PROV-JSONLD; flat but not linked-data |
| W3C PROV-O / RDF | `ogc.ogc-utils.prov.w3c-prov-rdf` | RDF (Turtle, N-Triples, RDF/XML, N-Quads, TriG, ...) | W3C Recommendation (PROV-O) | Full ontology binding; any RDF serialization applies |
| W3C PROV-JSONLD | `ogc.ogc-utils.prov.w3c-prov-jsonld` | JSON-LD (`@context`/`@graph`) | Non-normative (W3C Member Submission) | Linked-data JSON; flat `@graph` array of typed records |

## Cross-references to the OGC PROV Chain schema blocks

A separately maintained representation of the same PROV-O concepts - the **OGC PROV Chain** JSON
Schema family from [`bblock-prov-schema`](https://ogcincubator.github.io/bblock-prov-schema/) -
predates this repository and is reused here directly (`dependsOn`) rather than duplicated. It is,
in effect, **also a profile** of the same underlying PROV-O base as the five above: just JSON
Schema-structured (nested object graph, or flat array of full-IRI-referencing records) rather than
a `@context`/`@graph` linked-data document. The `w3c-prov-jsonld-to-ogc-prov-chain` /
`ogc-prov-chain-to-w3c-prov-jsonld` transforms (in `ogc.ogc-utils.prov.w3c-prov-jsonld`) losslessly
convert between it and W3C PROV-JSONLD precisely *because* both describe the same PROV-O
statements - that interoperability is the practical proof of the profile relationship, which is
now declared formally: `ogc.ogc-utils.prov.w3c-prov-jsonld` lists `ogc.ogc-utils.prov` in its own
`isProfileOf`, alongside this base block. The OGC PROV Chain register cannot reciprocate that
declaration (it is a pre-existing register we don't own, so we can't add metadata to it), but that
is an ownership limitation, not evidence the relationship is one-sided or conceptually different:

| Block | Identifier | Role |
|---|---|---|
| Provenance Chain | `ogc.ogc-utils.prov` | Top-level schema; a `Prov` mix-in accepting either a flat array of records or a single nested object |
| Single Schema for PROV | `ogc.ogc-utils.prov-bundled` | The original, pre-split single-schema PROV mix-in |
| Prov Entity | `ogc.ogc-utils.prov-entity` | Sub-schema for `Entity` records |
| Prov Activity | `ogc.ogc-utils.prov-activity` | Sub-schema for `Activity` records |
| Prov Agent | `ogc.ogc-utils.prov-agent` | Sub-schema for `Agent` records |

These model the same underlying concepts as the W3C representations above, but as JSON Schema:
either a nested/inline JSON object graph, or a flat array of full-IRI-referencing records - rather
than a flat statement list keyed by `@graph` like PROV-JSON/PROV-JSONLD. See:

- `ogc.ogc-utils.prov.w3c-prov-jsonld` for transforms between W3C PROV-JSONLD and the OGC PROV Chain
  array form;
- `ogc.ogc-utils.prov.ogc-prov-chain-forms` for transforms between OGC PROV Chain's own array and
  single-object forms.

## How everything interconnects

```
                     W3C PROV representations (this repo, all isProfileOf ogc.ogc-utils.prov.w3c-prov-base)
        ┌──────────┬───────────┬────────────┬─────────────┬───────────────┐
     PROV-N      PROV-XML   PROV-JSON    PROV-O/RDF    PROV-JSONLD
 (w3c-prov-n) (w3c-prov-xml) (w3c-prov-json) (w3c-prov-rdf) (w3c-prov-jsonld)
                                                             │
                                     w3c-prov-jsonld-to-ogc-prov-chain
                                     ogc-prov-chain-to-w3c-prov-jsonld
                                                             │
                                                             ▼
                                       OGC PROV Chain, ARRAY form  (ogc.ogc-utils.prov)
                                                             │
                                     ogc-prov-chain-array-to-object     (conditional)
                                     ogc-prov-chain-object-to-array     (always applicable)
                                     — both in ogc.ogc-utils.prov.ogc-prov-chain-forms —
                                                             │
                                                             ▼
                                      OGC PROV Chain, OBJECT form  (ogc.ogc-utils.prov)
```

Only W3C PROV-JSONLD currently has transforms to/from OGC PROV Chain (the `prov` Python library
used for these transforms doesn't natively expose the same round-trip for PROV-N/XML/JSON/RDF,
though it could in principle - see that block's description for details). The two OGC-internal
transforms are purely about OGC PROV Chain's own array/object duality and never touch any W3C
representation.

## Using this as an extension point

This block itself has no JSON Schema (see below for why), so it cannot declare `extensionPoints`
directly. But since it cross-references `ogc.ogc-utils.prov-entity`, `ogc.ogc-utils.prov-activity`
and `ogc.ogc-utils.prov-agent` - the exact sub-schemas that `ogc.ogc-utils.prov` references
internally - anyone wanting a *specialized* OGC PROV Chain profile (e.g. an `Entity` constrained to
a specific application schema) can use the
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

## Sources

* [PROV-Overview: An Overview of the PROV Family of Documents](https://www.w3.org/TR/prov-overview/)
* [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/)
* [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-prov-jsonld-alt](https://github.com/ogcincubator/bblocks-prov-jsonld-alt)
* Path: `_sources/prov/w3c-prov-base`

