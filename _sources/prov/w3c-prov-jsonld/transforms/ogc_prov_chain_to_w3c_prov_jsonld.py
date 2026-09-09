"""Convert an **OGC PROV Chain** document (``ogc.ogc-utils.prov``,
https://ogcincubator.github.io/bblock-prov-schema/), in its flat **array** form, into a
**W3C PROV-JSONLD** document (``@context``/``@graph``).

This transform assumes the exact input shape produced by
``w3c_prov_jsonld_to_ogc_prov_chain.py``: a bare top-level JSON array of flat ``Entity``/
``Activity``/``Agent`` objects, referencing each other by full-IRI ``id`` (no ``@context``,
no CURIEs, no inline-nested children). To convert a single-object/nested OGC PROV Chain
document instead, first run the ``ogc-prov-chain-object-to-array`` transform (see the
``ogc-prov-chain-forms`` block) to obtain this same flat-array shape, then chain into this
transform.

Scope: only the ``Entity``/``Activity``/``Agent`` core record types and the ``wasGeneratedBy``,
``used``, ``wasAssociatedWith``, ``wasAttributedTo``, ``wasDerivedFrom`` and ``actedOnBehalfOf``
relations are converted. Other PROV-DM relations/qualifications are not converted and are
silently dropped; extend ``_RELATION_PROPS``/the record-building loop below to cover more.
"""

import json
from urllib.parse import urlsplit

from prov.identifier import Namespace, QualifiedName
from prov.model import ProvDocument

_ACTIVITY_HINTS = ("startedAtTime", "endedAtTime", "used", "wasAssociatedWith", "activityType")
_AGENT_HINTS = ("actedOnBehalfOf", "agentType")
_RELATION_PROPS = (
    "wasGeneratedBy",
    "used",
    "wasAssociatedWith",
    "wasAttributedTo",
    "wasDerivedFrom",
    "actedOnBehalfOf",
)


def _record_kind(obj: dict) -> str:
    prov_type = obj.get("provType") or obj.get("prov:type") or obj.get("type")
    if prov_type:
        local = prov_type.rsplit(":", 1)[-1]
        if local in ("Entity", "Activity", "Agent", "Bundle", "Plan"):
            return "Activity" if local == "Activity" else ("Agent" if local == "Agent" else "Entity")
    if any(key in obj for key in _ACTIVITY_HINTS):
        return "Activity"
    if any(key in obj for key in _AGENT_HINTS):
        return "Agent"
    return "Entity"


def _refs(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _is_full_iri(value: str) -> bool:
    return isinstance(value, str) and bool(urlsplit(value).scheme)


def _split_namespace(uri: str) -> tuple:
    """Split a full IRI into (namespace_base, local_part) at its last '/' or '#'."""
    idx = max(uri.rfind("/"), uri.rfind("#"))
    return uri[: idx + 1], uri[idx + 1 :]


def _common_namespace(uris):
    """Longest shared namespace base (ending in '/' or '#') across a set of full IRIs."""
    if not uris:
        return None
    bases = [_split_namespace(u)[0] for u in uris]
    common = bases[0]
    for b in bases[1:]:
        while not b.startswith(common):
            common = common[:-1]
    idx = max(common.rfind("/"), common.rfind("#"))
    return common[: idx + 1] if idx >= 0 else None


class _IdentifierResolver:
    """Resolves full-IRI ``id`` strings to ``prov`` ``QualifiedName``s, registering as few
    namespaces as possible: a single shared namespace for IRIs with a common base, falling back
    to one namespace per distinct base otherwise.
    """

    def __init__(self, document: ProvDocument, all_ids):
        self._document = document
        self._shared_base = _common_namespace(list(all_ids))
        self._shared_ns = (
            document.add_namespace("ns0", self._shared_base) if self._shared_base else None
        )
        self._namespaces_by_base = {}

    def resolve(self, value):
        if value is None:
            return None
        base, local = _split_namespace(value)
        if self._shared_base and value.startswith(self._shared_base):
            return QualifiedName(self._shared_ns, value[len(self._shared_base) :])
        ns = self._namespaces_by_base.get(base)
        if ns is None:
            ns = Namespace(f"ns{len(self._namespaces_by_base) + 1}", base)
            self._document.add_namespace(ns)
            self._namespaces_by_base[base] = ns
        return QualifiedName(ns, local)


def convert(ogc_prov_chain_array_json: str) -> str:
    """Convert an OGC PROV Chain array document (as a string) to W3C PROV-JSONLD (as a string)."""
    chain = json.loads(ogc_prov_chain_array_json)
    if not isinstance(chain, list):
        raise ValueError(
            "ogc-prov-chain-to-w3c-prov-jsonld expects a bare top-level JSON array "
            "(the OGC PROV Chain 'array' form); got a single object instead. "
            "Run ogc-prov-chain-object-to-array first."
        )

    kinds = {obj["id"]: _record_kind(obj) for obj in chain if "id" in obj}
    ids_needing_resolution = set(kinds) | {
        target for obj in chain for prop in _RELATION_PROPS for target in _refs(obj.get(prop))
    }
    if not all(_is_full_iri(i) for i in ids_needing_resolution):
        raise ValueError(
            "ogc-prov-chain-to-w3c-prov-jsonld expects every 'id' to be a full IRI "
            "(as produced by w3c-prov-jsonld-to-ogc-prov-chain); CURIEs are not supported here."
        )

    document = ProvDocument()
    resolver = _IdentifierResolver(document, ids_needing_resolution)

    for obj in chain:
        identifier = obj.get("id")
        if identifier is None:
            continue
        qname = resolver.resolve(identifier)
        kind = kinds[identifier]
        if kind == "Activity":
            document.activity(qname, startTime=obj.get("startedAtTime"), endTime=obj.get("endedAtTime"))
        elif kind == "Agent":
            document.agent(qname)
        else:
            document.entity(qname)

    for obj in chain:
        identifier = obj.get("id")
        if identifier is None:
            continue
        subject = resolver.resolve(identifier)
        for target in _refs(obj.get("wasGeneratedBy")):
            document.wasGeneratedBy(subject, resolver.resolve(target))
        for target in _refs(obj.get("used")):
            document.used(subject, resolver.resolve(target))
        for target in _refs(obj.get("wasAssociatedWith")):
            document.wasAssociatedWith(subject, resolver.resolve(target))
        for target in _refs(obj.get("wasAttributedTo")):
            document.wasAttributedTo(subject, resolver.resolve(target))
        for target in _refs(obj.get("wasDerivedFrom")):
            document.wasDerivedFrom(subject, resolver.resolve(target))
        for target in _refs(obj.get("actedOnBehalfOf")):
            document.actedOnBehalfOf(subject, resolver.resolve(target))

    return document.serialize(format="jsonld", indent=2)


output_data = convert(input_data)
