"""Convert a **W3C PROV-XML** document into **W3C PROV-JSONLD** (``@context``/``@graph``),
using the `prov` library (https://prov.readthedocs.io/) as both the PROV-XML parser and the
PROV-JSONLD serializer.

The `prov` library's PROV-XML parser only understands XML produced by its own serializer (or
strictly XSD-conformant PROV-XML); hand-written or third-party PROV-XML using non-standard
element names for typed records may fail to parse - re-serialize such documents through
PROV-JSON or RDF first if this transform raises an error on otherwise-valid PROV-XML.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="xml")
output_data = document.serialize(format="jsonld")
