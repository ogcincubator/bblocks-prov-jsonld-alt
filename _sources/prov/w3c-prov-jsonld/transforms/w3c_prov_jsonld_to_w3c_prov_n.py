"""Convert a **W3C PROV-JSONLD** document (``@context``/``@graph``) into **W3C PROV-N**, using
the `prov` library (https://prov.readthedocs.io/) as the PROV-JSONLD parser and PROV-N
serializer.

There is intentionally no reverse (``w3c-prov-n-to-w3c-prov-jsonld``) transform: `prov`
implements a PROV-N *serializer* but not a parser (``ProvDocument.deserialize(..., format="provn")``
raises ``NotImplementedError``), so PROV-N can only ever be a transform *target* here, never a
source. To go from PROV-N to any other representation, use the PROV-N document's own
authoritative source data (e.g. its original PROV-JSON/XML/RDF form) directly instead.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="jsonld")
output_data = document.serialize(format="provn")
