"""Convert a "Provenance Chain" JSON document (``ogc.ogc-utils.prov``,
https://ogcincubator.github.io/bblock-prov-schema/) into a PROV-JSONLD document
(``@context``/``@graph``).

Scope mirrors ``to_provenance_chain.py``: only the ``Prov`` array of flat
``Entity``/``Activity``/``Agent`` objects, referencing each other by ``id``,
and the ``wasGeneratedBy``, ``used``, ``wasAssociatedWith``, ``wasAttributedTo``,
``wasDerivedFrom`` and ``actedOnBehalfOf`` relation properties are converted.
Inline-nested objects (``has_provenance``) are not expanded; flatten the input
to ID references before calling this transform if needed.
"""

import json

from prov.model import ProvDocument

_ACTIVITY_HINTS = ("startedAtTime", "endedAtTime", "used", "wasAssociatedWith", "activityType")
_AGENT_HINTS = ("actedOnBehalfOf", "agentType")


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


def convert(provenance_chain_json: str) -> str:
    """Convert a Provenance Chain document (as a string) to PROV-JSONLD (as a string)."""
    data = json.loads(provenance_chain_json)
    chain = data.get("Prov", data if isinstance(data, list) else [data])

    kinds = {obj["id"]: _record_kind(obj) for obj in chain if "id" in obj}

    document = ProvDocument()
    # Register any prefixes declared alongside the chain so that CURIE "id" references (e.g.
    # "ex:activity/step1") resolve, mirroring the "@context" convention used by Provenance Chain
    # examples (https://ogcincubator.github.io/bblock-prov-schema/).
    for prefix, uri in (data.get("@context") or {}).items():
        if isinstance(uri, str):
            document.add_namespace(prefix, uri)

    for obj in chain:
        identifier = obj.get("id")
        if identifier is None:
            continue
        kind = kinds[identifier]
        if kind == "Activity":
            document.activity(identifier, startTime=obj.get("startedAtTime"), endTime=obj.get("endedAtTime"))
        elif kind == "Agent":
            document.agent(identifier)
        else:
            document.entity(identifier)

    def _refs(value):
        if value is None:
            return []
        return value if isinstance(value, list) else [value]

    for obj in chain:
        identifier = obj.get("id")
        if identifier is None:
            continue
        for target in _refs(obj.get("wasGeneratedBy")):
            document.wasGeneratedBy(identifier, target)
        for target in _refs(obj.get("used")):
            document.used(identifier, target)
        for target in _refs(obj.get("wasAssociatedWith")):
            document.wasAssociatedWith(identifier, target)
        for target in _refs(obj.get("wasAttributedTo")):
            document.wasAttributedTo(identifier, target)
        for target in _refs(obj.get("wasDerivedFrom")):
            document.wasDerivedFrom(identifier, target)
        for target in _refs(obj.get("actedOnBehalfOf")):
            document.actedOnBehalfOf(identifier, target)

    return document.serialize(format="jsonld", indent=2)


output_data = convert(input_data)
