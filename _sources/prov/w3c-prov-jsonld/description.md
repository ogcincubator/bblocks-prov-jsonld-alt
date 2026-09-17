# W3C PROV-JSONLD

PROV-JSONLD is a non-normative W3C Member Submission JSON-LD binding of PROV-DM: a single
context (this repository plus the vocabulary at the referenced `context.jsonld`) and a flat
graph array of typed records — as opposed to the nested "Provenance Chain" representation from
`bblock-prov-schema`'s [`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov) (OGC PROV Chain) (see
the Transforms tab below) or the flat but non-linked-data
[`ogc.ogc-utils.prov.w3c-prov-json`](bblocks://ogc.ogc-utils.prov.w3c-prov-json) (W3C PROV-JSON).

`schema` and `ldContext` reference the authoritative documents directly rather than vendoring
copies, so this block always tracks the upstream submission.

## `prov:mentionOf` / bundle mentions

The `prov` Python library's native PROV-JSONLD serializer does not support `prov:Mention` /
`prov:mentionOf` (it raises `ProvJSONLDException`) — those terms were removed from PROV-DM's final
Recommendation and now live only in the non-normative
[PROV-Links](https://www.w3.org/TR/prov-links/) note. The example below shows the accepted
workaround: `prov:specializationOf` plus a plain `prov:asInBundle` attribute, which serializes
correctly in every PROV representation, including PROV-JSONLD.

## Transforms

This block acts as the **hub** for converting between W3C PROV representations and between W3C
PROV and OGC PROV Chain: every transform either converts something *into* PROV-JSONLD or
converts PROV-JSONLD *into* something else, all implemented in Python using the `prov` library
and explicitly named for the two representations each one bridges. See the
[Transforms tab](https://ogcincubator.github.io/bblocks-docs/create/transforms) on this block's
page for the full, current list with examples.

**Bridging to OGC PROV Chain:**

- **W3C PROV-JSONLD → OGC PROV Chain**: converts a W3C PROV-JSONLD document into the flat
  **array** form of OGC PROV Chain (validated against
  [`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov)). Always emits the array form with
  full-IRI identifiers, since a generic converter can't assume a single natural root exists for
  arbitrary input.
- **OGC PROV Chain → W3C PROV-JSONLD**: converts the flat array form of an OGC PROV Chain
  document back into W3C PROV-JSONLD.

If a single-object OGC PROV Chain result is needed instead of the array form, chain the first
transform's output into the array→object transform from
[`ogc.ogc-utils.prov.ogc-prov-chain-forms`](bblocks://ogc.ogc-utils.prov.ogc-prov-chain-forms)
(OGC PROV Chain: Array ⇄ Object Conversion) - that block also provides the reverse (object→array)
for feeding a single-object document into the OGC PROV Chain → W3C PROV-JSONLD transform above.
That block's description explains why array→object is only conditionally applicable while
object→array always is.

**Bridging to/from the other W3C PROV representations:**

| Direction | Notes |
|---|---|
| PROV-JSON ⇄ PROV-JSONLD | Bidirectional |
| PROV-O/RDF (Turtle) ⇄ PROV-JSONLD | Bidirectional |
| PROV-XML ⇄ PROV-JSONLD | Bidirectional |
| PROV-JSONLD → PROV-N | One-way only |

Combining these with the OGC PROV Chain transforms above gives every W3C PROV representation a
path to and from OGC PROV Chain via PROV-JSONLD as an intermediate step - e.g. PROV-XML → PROV-JSONLD
→ OGC PROV Chain (array) → (optionally) OGC PROV Chain (object), without needing a separate
direct transform for every pair of representations. Every W3C PROV representation also has direct
transforms to every other one (see each format block's own Transforms tab, and the interconnection
table in [`ogc.ogc-utils.prov.w3c-prov-base`](bblocks://ogc.ogc-utils.prov.w3c-prov-base)) - the
PROV-JSONLD hub above remains the only path to/from OGC PROV Chain specifically.

**PROV-N is a one-way exception:** `prov` implements a PROV-N *serializer* but not a *parser*
(deserializing PROV-N raises `NotImplementedError`), so no transform here (or anywhere in this
repository) can take PROV-N as input. To convert data available only as PROV-N into another
representation, start from that data's original PROV-JSON/XML/RDF source instead, if available.

**Note on the RDF→PROV-JSONLD transform and QName-unsafe identifiers:** `prov`'s RDF
deserializer requires every prefixed name (CURIE) it re-derives while reading Turtle to be
coercible to an XML `QName`/NCName local part, which must start with a letter or underscore and
cannot contain `/`, `#`, or `:`. Some real-world identifiers are not QName-safe under their
natural namespace split - e.g. `doi:10.5281/zenodo.14210717` (a slash in the local part) or
SHA1/SHA256 hash-based identifiers such as `data:644e201526525f62152815a76a2dc773450f3dd9` (a
digit-leading local part, common since hex digests often start with `0`-`9`). The
`example-ogcapi-processes-job` example's regeneration script sanitizes the local part of every
such identifier in place (e.g. `644e201526525f62152815a76a2dc773450f3dd9` ->
`_644e201526525f62152815a76a2dc773450f3dd9`), **keeping each identifier's original namespace
unchanged** rather than splitting off a new, narrower one: introducing many one-off sub-namespaces
that overlap an existing broader namespace was found to make `prov`'s namespace reconciliation
ambiguous, non-deterministically corrupting RDF re-serialization. The fix is applied to every
occurrence of the identifier (both as a record identifier and as any attribute value referencing
it), so every representation - including this transform - round-trips it correctly.
