"""Convert a **W3C PROV-JSON** document into **W3C PROV-XML**, using the `prov` library
(https://prov.readthedocs.io/) as both the PROV-JSON parser and the PROV-XML serializer - a
direct conversion, not chained through PROV-JSONLD.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="json")
output_data = document.serialize(format="xml")
