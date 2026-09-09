"""Convert a **W3C PROV-JSON** document into **W3C PROV-JSONLD** (``@context``/``@graph``),
using the `prov` library (https://prov.readthedocs.io/) as both the PROV-JSON parser and the
PROV-JSONLD serializer - no manual graph manipulation involved on either side.

Known caveat - literal vs. resource-typed values: an attribute such as ``prov:location`` declared
as a plain untyped string in PROV-JSON (rather than ``{"$": "...", "type": "prov:QUALIFIED_NAME"}``
or ``xsd:anyURI``) stays a plain string/literal all the way through to RDF once this document is
later converted to Turtle, even though the value looks like a URI. If a downstream RDF profile
expects that property to be a resource (IRI), the source PROV-JSON should type the value
explicitly rather than leaving it a bare string (see the ``example-ogcapi-processes-job`` example
fixtures in this repository, which apply exactly this fix to their ``prov:location`` values).
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="json")
output_data = document.serialize(format="jsonld")
