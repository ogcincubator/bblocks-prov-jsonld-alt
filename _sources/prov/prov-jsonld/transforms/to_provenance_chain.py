"""Convert a PROV-JSONLD document (``@context``/``@graph``) into the nested
"Provenance Chain" JSON representation defined by ``ogc.ogc-utils.prov``
(https://ogcincubator.github.io/bblock-prov-schema/).

Scope: this is intentionally limited to the record types and relations most
commonly produced by PROV tooling (e.g. cwltool): ``Entity``/``Activity``/
``Agent`` core records plus the ``wasGeneratedBy``, ``used``,
``wasAssociatedWith``, ``wasAttributedTo``, ``wasDerivedFrom`` and
``actedOnBehalfOf`` relations. Other PROV-DM relations/qualifications are not
converted and are silently dropped; extend ``_RELATION_HANDLERS`` below to
cover more.

Objects are emitted as a flat list with relations expressed as ID references
(the "Provenance Chain" schema allows both inline nesting and ID references
via ``objectref`` for every relation) rather than nesting related objects
inline, which keeps the conversion a straightforward, invertible mapping.
"""

import json

from prov.model import ProvDocument, ProvRelation
from prov.constants import (
    PROV_TYPE,
    PROV_GENERATION,
    PROV_USAGE,
    PROV_ASSOCIATION,
    PROV_ATTRIBUTION,
    PROV_DERIVATION,
    PROV_DELEGATION,
)

# Maps a PROV relation type to the (provenance-chain property, subject role, object role)
# used to fold that relation into the referencing record, e.g. wasGeneratedBy is folded
# into the Entity that is the relation's "entity".
_RELATION_HANDLERS = {
    PROV_GENERATION: ("wasGeneratedBy", "entity", "activity"),
    PROV_USAGE: ("used", "activity", "entity"),
    PROV_ASSOCIATION: ("wasAssociatedWith", "activity", "agent"),
    PROV_ATTRIBUTION: ("wasAttributedTo", "entity", "agent"),
    PROV_DERIVATION: ("wasDerivedFrom", "generatedEntity", "usedEntity"),
    PROV_DELEGATION: ("actedOnBehalfOf", "delegate", "responsible"),
}

_RECORD_TYPE_FIELD = {
    "Entity": "provType",
    "Activity": "provType",
    "Agent": "provType",
}


def _qname_str(value):
    """Render a prov QualifiedName/identifier/literal as a plain string ref."""
    if value is None:
        return None
    return str(value)


def convert(prov_jsonld: str) -> str:
    """Convert a PROV-JSONLD document (as a string) to Provenance Chain JSON (as a string)."""
    document = ProvDocument.deserialize(content=prov_jsonld, format="jsonld")

    objects_by_id = {}
    order = []

    def get_or_create(identifier, prov_type):
        key = str(identifier)
        if key not in objects_by_id:
            objects_by_id[key] = {"id": key, _RECORD_TYPE_FIELD[prov_type]: prov_type}
            order.append(key)
        return objects_by_id[key]

    for record in document.get_records():
        record_type = record.get_type().localpart if record.get_type() else None
        if record_type in ("Entity", "Activity", "Agent") and record.identifier is not None:
            get_or_create(record.identifier, record_type)

    for record in document.get_records(ProvRelation):
        handler = _RELATION_HANDLERS.get(record.get_type())
        if handler is None:
            continue
        prop, subject_role, object_role = handler
        # formal_attributes keys are QualifiedName objects (e.g. prov:activity); match by localpart.
        formal = {key.localpart: value for key, value in record.formal_attributes}
        subject_id = _qname_str(formal.get(subject_role) or formal.get("entity") or formal.get("activity"))
        object_id = _qname_str(formal.get(object_role))
        if subject_id is None or object_id is None:
            continue
        subject_obj = objects_by_id.get(subject_id)
        if subject_obj is None:
            # Relation referencing a record not declared as Entity/Activity/Agent in this
            # document (e.g. cross-bundle reference) - skip, nothing to attach it to.
            continue
        existing = subject_obj.get(prop)
        if existing is None:
            subject_obj[prop] = object_id
        elif isinstance(existing, list):
            if object_id not in existing:
                existing.append(object_id)
        elif existing != object_id:
            subject_obj[prop] = [existing, object_id]

    chain = [objects_by_id[key] for key in order]
    result = {"Prov": chain}

    # Carry over the source document's custom prefixes as a "@context" so that the CURIE-form
    # "id" references above stay resolvable (Provenance Chain examples use the same convention,
    # see https://ogcincubator.github.io/bblock-prov-schema/).
    prefixes = {
        ns.prefix: ns.uri
        for ns in document.get_registered_namespaces()
        if ns.prefix not in ("prov", "xsd")
    }
    if prefixes:
        result["@context"] = prefixes

    return json.dumps(result, indent=2)


output_data = convert(input_data)
