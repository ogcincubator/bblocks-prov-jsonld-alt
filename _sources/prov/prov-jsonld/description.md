# PROV-JSONLD

PROV-JSONLD is a non-normative W3C Member Submission JSON-LD binding of PROV-DM: a single
`@context` (this repository plus the vocabulary at the referenced `context.jsonld`) and a flat
`@graph` array of typed records — as opposed to the nested "Provenance Chain" representation from
[`bblock-prov-schema`](bblocks://ogc.ogc-utils.prov) (see the
[transform](#transforms) below) or the flat but non-linked-data
[PROV-JSON](bblocks://ogc.ogc-utils.prov.prov-json).

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

This block declares a `to-provenance-chain` transform converting a PROV-JSONLD document into the
nested "Provenance Chain" JSON representation (validated against
[`ogc.ogc-utils.prov`](bblocks://ogc.ogc-utils.prov)), and a `from-provenance-chain` transform for
the reverse direction. Both are implemented in Python using the `prov` library's PROV-JSONLD
(de)serializer.
