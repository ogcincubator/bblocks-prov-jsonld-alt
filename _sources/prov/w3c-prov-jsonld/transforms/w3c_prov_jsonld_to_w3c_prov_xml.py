"""Convert a **W3C PROV-JSONLD** document (``@context``/``@graph``) into **W3C PROV-XML**,
using the `prov` library (https://prov.readthedocs.io/) as both the PROV-JSONLD parser and the
PROV-XML serializer.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="jsonld")
output_data = document.serialize(format="xml")
