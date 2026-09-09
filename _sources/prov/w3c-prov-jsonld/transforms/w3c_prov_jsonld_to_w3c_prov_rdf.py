"""Convert a **W3C PROV-JSONLD** document (``@context``/``@graph``) into **W3C PROV-O / RDF**
(Turtle), using the `prov` library (https://prov.readthedocs.io/), which parses PROV-JSONLD
natively and serializes RDF via `rdflib`.

Known caveat - literal vs. resource-typed values: attributes such as ``prov:atLocation`` that are
plain untyped strings in the source (rather than a ``prov:QUALIFIED_NAME``/``xsd:anyURI``-typed
value referencing a namespace) are carried through as RDF *literals*, not IRI resources. This is
valid PROV-O, but stricter profiles (e.g. SHACL shapes requiring ``sh:nodeKind sh:IRI`` on that
property) will reject it. If the source data intends such a value to identify a resource, type it
as a qualified name/IRI before conversion rather than a bare string (see the
``example-ogcapi-processes-job`` example fixtures in this repository, which apply exactly this
fix to their ``prov:location`` values).
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="jsonld")
output_data = document.serialize(format="rdf", rdf_format="turtle")
