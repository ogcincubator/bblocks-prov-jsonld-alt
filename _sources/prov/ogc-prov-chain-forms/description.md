# OGC PROV Chain: Array ⇄ Object Conversion

The **OGC PROV Chain** JSON Schema (`ogc.ogc-utils.prov`, from
[`bblock-prov-schema`](https://ogcincubator.github.io/bblock-prov-schema/)) allows a document to
take either of two shapes:

- a flat top-level **array** of `Entity`/`Activity`/`Agent` records, each referencing others by
  `id` (the `Prov` branch of the schema's top-level `anyOf`);
- a single-**object** document, where one record is the root and its related records are
  inlined directly into its relation properties (`wasGeneratedBy`, `used`,
  `wasAssociatedWith`, ...) and/or listed alongside it via `has_provenance`.

Both shapes describe the same underlying records and relations; this block provides two
transforms to convert between them:

| Transform | Direction | Applicability |
|---|---|---|
| `ogc-prov-chain-object-to-array` | object → array | Always applicable |
| `ogc-prov-chain-array-to-object` | array → object | Conditional - only when the array reduces to a single natural root |

> **Not involving W3C PROV.** Both the input and output of both transforms are OGC PROV Chain
> documents - neither W3C PROV-JSONLD nor any other W3C PROV representation is read or produced
> here. For converting a W3C PROV-JSONLD document into OGC PROV Chain (and back), see the
> `w3c-prov-jsonld-to-ogc-prov-chain` / `ogc-prov-chain-to-w3c-prov-jsonld` transforms declared on
> the `ogc.ogc-utils.prov.w3c-prov-jsonld` block instead - those two blocks can be chained with the
> ones here if a single-object (rather than array) OGC PROV Chain result is wanted.

## Why array → object is only conditional

Flattening (object → array) never loses information: every inlined record simply becomes its
own top-level array entry. Nesting (array → object), however, requires picking a single record
to be the root that everything else hangs off of. A root only exists when exactly one record in
the array is never referenced as a relation target by any other record, and every other record
is reachable from it without revisiting one already inlined elsewhere. An arbitrary array (e.g.
one with several disconnected subgraphs, or none/multiple candidate roots) has no such natural
single-object form. When that's the case, `ogc-prov-chain-array-to-object` raises a descriptive
error rather than guessing - callers should treat that as "not applicable to this input" and
keep the array form instead.

## How this fits with the rest of the repository

See `ogc.ogc-utils.prov.w3c-prov-base` ("W3C PROV Representation Base") for a diagram of how this block,
the W3C PROV representation profiles, and the OGC PROV Chain schema blocks all interconnect.
