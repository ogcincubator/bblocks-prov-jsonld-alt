"""Convert a **W3C PROV-O / RDF** document (Turtle) into **W3C PROV-JSONLD**
(``@context``/``@graph``), using the `prov` library (https://prov.readthedocs.io/), which
parses RDF via `rdflib` and serializes PROV-JSONLD natively.

Only the PROV-DM information `rdflib`/`prov` can recover from generic RDF triples survives
this round trip - PROV-N-only constructs with no RDF binding (if any) are not represented in
Turtle to begin with, so nothing is lost here that wasn't already absent from the input.

Known limitation - QName-unsafe CURIEs: on deserialization, `prov` tries to compact *every* URI
matching a namespace prefix declared anywhere in the input Turtle (even an unused `@prefix` line)
into an XML `QName`/NCName local part, which (per the XML Name grammar) must start with a letter
or underscore and cannot contain ``/``, ``#``, or ``:``. This affects more identifiers than it
first appears:

- Slash-containing locals, e.g. ``doi:10.5281/zenodo.14210717`` (namespace ``doi: https://doi.org/``).
- Digit-leading locals, e.g. ``data:644e201526525f62152815a76a2dc773450f3dd9`` (namespace
  ``data: urn:hash::sha1:``) - common for hash-based identifiers, since hex digests frequently
  start with a digit ``0``-``9``.

Both shapes make this transform raise ``ProvExceptionInvalidQualifiedName``, and - because `prov`'s
internal attribute sets are unordered (iteration order depends on Python's per-process hash seed) -
*which* offending identifier surfaces first can vary from run to run of the very same input file.

If you control the document being converted, avoid the failure by sanitizing the local part of
every affected identifier so it is QName-safe (non-empty, starts with a letter/underscore,
contains none of ``/ # :``), e.g. ``644e201526525f62152815a76a2dc773450f3dd9`` ->
``_644e201526525f62152815a76a2dc773450f3dd9``. **Keep the identifier's original namespace
unchanged** rather than splitting off a new, narrower one - introducing many one-off sub-namespaces
that overlap an existing broader namespace (e.g. a per-identifier ``urn:hash::sha1:644`` alongside
the original, broader ``data: urn:hash::sha1:``) creates an ambiguous "longest prefix match" during
`prov`'s namespace reconciliation, which was observed to non-deterministically corrupt RDF
re-serialization (emitting a bogus ``<prefix:local>`` as a literal IRI instead of expanding it).
This must be applied to every occurrence of the identifier in the document (both as a record
identifier and as any attribute value referencing it), not just its point of definition. See the
``example-ogcapi-processes-job`` example fixtures in this repository, which apply exactly this fix.
"""

from prov.model import ProvDocument

document = ProvDocument.deserialize(content=input_data, format="rdf", rdf_format="turtle")
output_data = document.serialize(format="jsonld")
