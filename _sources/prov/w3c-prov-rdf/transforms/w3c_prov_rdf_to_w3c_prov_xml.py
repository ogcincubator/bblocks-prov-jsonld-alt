"""Convert a **W3C PROV-O / RDF** document (Turtle) into **W3C PROV-XML**, using the `prov`
library (https://prov.readthedocs.io/), which parses RDF via `rdflib` and serializes PROV-XML
natively - a direct conversion, not chained through PROV-JSONLD.

Known caveats when parsing RDF into `prov`'s data model, both discovered against the
``example-ogcapi-processes-job`` example fixtures in this repository (see their source Turtle
for concrete instances) and applicable regardless of the RDF-to-non-RDF target format:

- **QName-unsafe identifiers.** RDF identifiers whose local name would not be a valid XML QName
  local part (starting with a digit, or containing ``/``, ``#`` or ``:``, e.g. SHA1-hash-based
  ``data:`` identifiers) must be sanitized *in place* before being handed to `prov` - prepend
  ``_`` if the local part doesn't start with a letter/underscore, and replace any embedded
  ``/``, ``#``, ``:`` with ``_`` - while keeping the identifier's namespace unchanged. Do not
  invent narrow per-identifier namespaces instead: overlapping/ambiguous namespaces make
  `prov`'s ``NamespaceManager`` prefix resolution non-deterministic on re-serialization.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="rdf", rdf_format="turtle")
output_data = document.serialize(format="xml")
