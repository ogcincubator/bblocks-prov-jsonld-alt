"""Convert a **W3C PROV-XML** document into **W3C PROV-O / RDF** (Turtle), using the `prov`
library (https://prov.readthedocs.io/) as the PROV-XML parser and `rdflib` (via `prov`'s RDF
serializer) for Turtle output - a direct conversion, not chained through PROV-JSONLD.

Same PROV-XML parsing caveat as `w3c-prov-xml-to-w3c-prov-json`: only XML produced by `prov`
itself, or strictly XSD-conformant PROV-XML, is guaranteed to parse.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="xml")
output_data = document.serialize(format="rdf", rdf_format="turtle")
