
# OGC PROV Chain: Array ⇄ Object Conversion (Model)

`ogc.ogc-utils.prov.ogc-prov-chain-forms` *v0.1*

Two transforms that convert an **OGC PROV Chain** document (`ogc.ogc-utils.prov`, from https://ogcincubator.github.io/bblock-prov-schema/) between its two allowed shapes: a flat top-level **array** (every record referencing others by full-IRI `id`) and a nested single **object** (one root record with related records inlined). Both shapes validate against the same imported `ogc.ogc-utils.prov` schema. Purely internal to OGC PROV Chain - no W3C PROV representation is involved here; see `ogc.ogc-utils.prov.w3c-prov-jsonld` for the transforms that bridge to/from W3C PROV-JSONLD.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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

## Examples

### OGC PROV Chain, flat array form (every record referencing others by full-IRI id)
#### json
```json
[
  {
    "id": "https://example.org/cwlprov/entities/output",
    "provType": "Entity",
    "wasGeneratedBy": "https://example.org/cwlprov/activities/run"
  },
  {
    "id": "https://example.org/cwlprov/activities/run",
    "provType": "Activity",
    "startedAtTime": "2024-03-01T09:00:00Z",
    "endedAtTime": "2024-03-01T09:05:00Z",
    "used": "https://example.org/cwlprov/entities/input",
    "wasAssociatedWith": "https://example.org/cwlprov/agents/user"
  },
  {
    "id": "https://example.org/cwlprov/entities/input",
    "provType": "Entity"
  },
  {
    "id": "https://example.org/cwlprov/agents/user",
    "provType": "Agent"
  }
]

```


### OGC PROV Chain, single-object form (relation targets inlined from a single root)
#### json
```json
{
  "id": "https://example.org/cwlprov/entities/output",
  "provType": "Entity",
  "wasGeneratedBy": {
    "id": "https://example.org/cwlprov/activities/run",
    "provType": "Activity",
    "startedAtTime": "2024-03-01T09:00:00Z",
    "endedAtTime": "2024-03-01T09:05:00Z",
    "used": {
      "id": "https://example.org/cwlprov/entities/input",
      "provType": "Entity"
    },
    "wasAssociatedWith": {
      "id": "https://example.org/cwlprov/agents/user",
      "provType": "Agent"
    }
  }
}
```


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-prov-jsonld-alt](https://github.com/ogcincubator/bblocks-prov-jsonld-alt)
* Path: `_sources/prov/ogc-prov-chain-forms`

