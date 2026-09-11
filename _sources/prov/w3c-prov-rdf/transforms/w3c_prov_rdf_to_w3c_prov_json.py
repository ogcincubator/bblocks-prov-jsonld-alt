"""Convert a **W3C PROV-O / RDF** document (Turtle) into **W3C PROV-JSON**, using the `prov`
library (https://prov.readthedocs.io/), which parses RDF via `rdflib` and serializes PROV-JSON
natively - a direct conversion, not chained through PROV-JSONLD.

Same QName-unsafe identifier caveat as `w3c-prov-rdf-to-w3c-prov-xml` (sanitize the local part
in place, keep the original namespace) - see that transform's docstring for details.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="rdf", rdf_format="turtle")
output_data = document.serialize(format="json")
