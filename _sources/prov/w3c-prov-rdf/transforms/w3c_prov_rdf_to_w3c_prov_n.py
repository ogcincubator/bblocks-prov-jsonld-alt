"""Convert a **W3C PROV-O / RDF** document (Turtle) into **W3C PROV-N**, using the `prov` library
(https://prov.readthedocs.io/), which parses RDF via `rdflib` and serializes PROV-N natively - a
direct conversion, not chained through PROV-JSONLD.

Same QName-unsafe identifier caveat as `w3c-prov-rdf-to-w3c-prov-xml` applies to parsing. There is
intentionally no reverse (``w3c-prov-n-to-w3c-prov-rdf``) transform: `prov` implements a PROV-N
*serializer* but not a parser, so PROV-N can only ever be a transform *target*, never a source
(see `w3c-prov-jsonld-to-w3c-prov-n` for the same caveat).
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="rdf", rdf_format="turtle")
output_data = document.serialize(format="provn")
