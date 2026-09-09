"""Nest a flat top-level **array** form **OGC PROV Chain** document (``ogc.ogc-utils.prov``,
https://ogcincubator.github.io/bblock-prov-schema/) into its single-**object** form, by
inlining relation targets recursively from a single detected root record.

This transform is purely internal to OGC PROV Chain: both the input (flat array, every record
referencing others by ``id``) and the output (single object, with related records inlined into
its relation properties) validate against the same ``ogc.ogc-utils.prov`` schema. It does not
involve W3C PROV-JSONLD or any other W3C PROV representation.

This direction is only **conditionally applicable**: a root is only detected when exactly one
record in the array is never referenced as a relation target by any other record (an
"in-degree zero" node), and every other record is reachable from it by following relation
properties without revisiting a record already inlined elsewhere. If zero or more than one such
root exists, or the graph is disconnected/cyclic, this raises a ``ValueError`` describing why -
callers should treat that as "not applicable to this input" rather than a transform bug. The
reverse direction (``ogc-prov-chain-object-to-array``) is always applicable.

Records reachable from the root through more than one path (e.g. two records both relating to
the same shared target) are inlined only the *first* time they're reached; subsequent
references to them are left as plain ``id`` strings, since a JSON object can't repeat the same
inlined content in two places without duplication.
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


def convert(ogc_prov_chain_array_json: str) -> str:
    """Convert a flat-array OGC PROV Chain document (as a string) to its single-object,
    inline-nested form (as a string)."""
    chain = json.loads(ogc_prov_chain_array_json)
    if not isinstance(chain, list):
        raise ValueError(
            "ogc-prov-chain-array-to-object expects a bare top-level JSON array "
            "(the OGC PROV Chain 'array' form); got a single object instead - it is already nested."
        )

    records = {record["id"]: record for record in chain if "id" in record}

    in_degree = {identifier: 0 for identifier in records}
    for record in records.values():
        for prop in _RELATION_PROPS:
            for target in _values(record.get(prop)):
                if target in in_degree:
                    in_degree[target] += 1

    roots = [identifier for identifier, degree in in_degree.items() if degree == 0]
    if len(roots) != 1:
        raise ValueError(
            "ogc-prov-chain-array-to-object is not applicable to this input: expected exactly "
            f"one record with no incoming relation references (found {len(roots)}: {roots}). "
            "The array does not reduce to a single natural root - keep it in array form, or "
            "restructure it so a single record is never referenced by any other."
        )

    inlined = set()

    def build(identifier: str) -> dict:
        record = records[identifier]
        inlined.add(identifier)
        node = dict(record)
        for prop in _RELATION_PROPS:
            if prop not in node:
                continue
            targets = _values(node[prop])
            resolved = []
            for target in targets:
                if target in records and target not in inlined:
                    resolved.append(build(target))
                else:
                    resolved.append(target)
            node[prop] = resolved[0] if len(targets) == 1 else resolved
        return node

    root_object = build(roots[0])

    unreachable = set(records) - inlined
    if unreachable:
        raise ValueError(
            "ogc-prov-chain-array-to-object is not applicable to this input: "
            f"{len(unreachable)} record(s) are not reachable from the single root {roots[0]!r} "
            f"by following relation properties: {sorted(unreachable)}. "
            "The array likely contains a disconnected component or a relation cycle."
        )

    return json.dumps(root_object, indent=2)


output_data = convert(input_data)
