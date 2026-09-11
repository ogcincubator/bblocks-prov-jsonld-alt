"""Convert a **W3C PROV-XML** document into **W3C PROV-N**, using the `prov` library
(https://prov.readthedocs.io/) as the PROV-XML parser and PROV-N serializer - a direct
conversion, not chained through PROV-JSONLD.

There is intentionally no reverse (``w3c-prov-n-to-w3c-prov-xml``) transform: `prov` implements
a PROV-N *serializer* but not a parser, so PROV-N can only ever be a transform *target*, never a
source (see `w3c-prov-jsonld-to-w3c-prov-n` for the same caveat).
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="xml")
output_data = document.serialize(format="provn")
