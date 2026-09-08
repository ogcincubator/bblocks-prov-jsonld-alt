# PROV-N

PROV-N is a textual, human-readable notation for PROV-DM instances. It has no JSON Schema of its
own (see the [base block](bblocks://ogc.ogc-utils.prov.base) for why); this block exists only to
register PROV-N as a first-class representation profile, with an example for cross-reference and
round-trip testing against the other profiles via the `prov` library's PROV-N parser/serializer.
