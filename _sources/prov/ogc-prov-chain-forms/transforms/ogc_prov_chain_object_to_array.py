"""Flatten a single-**object** form **OGC PROV Chain** document (``ogc.ogc-utils.prov``,
https://ogcincubator.github.io/bblock-prov-schema/) into its flat top-level **array** form.

This transform is purely internal to OGC PROV Chain: both the input (single-object, possibly
with inline-nested relation targets and/or a ``has_provenance`` sibling list) and the output
(flat array, every record referencing others by ``id``) validate against the same
``ogc.ogc-utils.prov`` schema. It does not involve W3C PROV-JSONLD or any other W3C PROV
representation.

This direction is **always applicable**: any single-object OGC PROV Chain document, however
deeply nested, can be flattened. The reverse direction
(``ogc-prov-chain-array-to-object``) is only conditionally applicable, since a flat array does
not always reduce to a single natural root.

If the input declares a top-level ``@context`` with simple ``"prefix": "http://...#/"``
mappings, CURIE ``id``/reference values are expanded to full IRIs using it, since the flat
array form has no room for a sibling ``@context`` (the same convention used by
``w3c_prov_jsonld_to_ogc_prov_chain.py``). Any other ``@context`` shape (e.g. per-term
``@context`` overrides) is left unresolved; ids that aren't found are copied through unchanged.
"""

import json

_RELATION_PROPS = (
    "wasGeneratedBy",
    "used",
    "wasAssociatedWith",
    "wasAttributedTo",
    "wasDerivedFrom",
    "actedOnBehalfOf",
)


def _values(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _make_expander(context: dict):
    prefixes = {k: v for k, v in context.items() if isinstance(v, str)}

    def expand(value):
        if not isinstance(value, str) or ":" not in value:
            return value
        prefix, _, local = value.partition(":")
        base = prefixes.get(prefix)
        return f"{base}{local}" if base else value

    return expand


def convert(ogc_prov_chain_object_json: str) -> str:
    """Convert a single-object OGC PROV Chain document (as a string) to its flat array form
    (as a string)."""
    data = json.loads(ogc_prov_chain_object_json)
    if not isinstance(data, dict):
        raise ValueError(
            "ogc-prov-chain-object-to-array expects a single top-level JSON object "
            "(the OGC PROV Chain 'object' form); got an array instead - it is already flat."
        )

    expand = _make_expander(data.get("@context") or {})
    flattened = {}
    order = []

    def flatten(record: dict) -> str:
        """Recursively flatten `record` (and everything reachable through its relation
        properties / has_provenance), returning the (expanded) id of `record` itself."""
        record_id = expand(record.get("id"))
        flat = {k: v for k, v in record.items() if k not in ("@context", "has_provenance")}
        flat["id"] = record_id

        for prop in _RELATION_PROPS:
            if prop not in flat:
                continue
            targets = []
            for target in _values(flat[prop]):
                if isinstance(target, dict):
                    targets.append(flatten(target))
                else:
                    targets.append(expand(target))
            flat[prop] = targets[0] if len(targets) == 1 else targets

        if record_id not in flattened:
            flattened[record_id] = flat
            order.append(record_id)
        for nested in _values(record.get("has_provenance")):
            if isinstance(nested, dict):
                flatten(nested)

        return record_id

    flatten(data)
    chain = [flattened[key] for key in order]
    return json.dumps(chain, indent=2)


output_data = convert(input_data)
