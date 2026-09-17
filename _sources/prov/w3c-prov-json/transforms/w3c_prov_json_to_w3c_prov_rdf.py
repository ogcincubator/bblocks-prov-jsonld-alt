"""Convert a **W3C PROV-JSON** document into **W3C PROV-O / RDF** (Turtle), using the `prov`
library (https://prov.readthedocs.io/) as the PROV-JSON parser and `rdflib` (via `prov`'s RDF
serializer) for Turtle output - a direct conversion, not chained through PROV-JSONLD.

Known caveat - literal vs. resource-typed values: as with `w3c-prov-json-to-w3c-prov-jsonld`, an
attribute such as ``prov:location`` declared as a plain untyped string in PROV-JSON (rather than
``{"$": "...", "type": "prov:QUALIFIED_NAME"}`` or ``xsd:anyURI``) is carried through to RDF as a
plain literal rather than a resource (IRI), even if the value looks like a URI. Type the source
value explicitly in PROV-JSON if a downstream RDF profile expects a resource there (see the
``example-ogcapi-processes-job`` example fixtures in this repository).
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="json")
output_data = document.serialize(format="rdf", rdf_format="turtle")
