# W3C PROV-O / RDF

PROV-O maps every PROV-DM concept directly onto RDF classes/properties, so this block is an
[RDF-only block](https://ogcincubator.github.io/bblocks-docs/create/rdf-only): no JSON Schema,
`ontology` points at the PROV-O document, and the example below is Turtle.

The example illustrates a nuance also relevant to
[`ogc.ogc-utils.prov.w3c-prov-jsonld`](bblocks://ogc.ogc-utils.prov.w3c-prov-jsonld)
(W3C PROV-JSONLD): an `Association` qualified with extra attributes (here, `prov:hadPlan`) is
reified as a blank node (`prov:qualifiedAssociation`) *and*, separately, a plain
`prov:wasAssociatedWith` shortcut triple is still needed on the activity for tools that only read
the shortcut property.

## Note on the OGC API - Processes example's `prov:atLocation` values

The source PROV-JSON fixture behind `example-ogcapi-processes-job` declares its `prov:location`
values as plain untyped strings (e.g. `"https://hirondelle.crim.ca/weaver"`), which `prov` would
by default carry through as RDF literals. PROV-O's `prov:atLocation` expects a resource (an IRI or
blank node), not a literal, so this example's regeneration script re-types each such value as a
proper IRI (splitting the URI into a namespace + local part and registering it as a
`QualifiedName`) rather than leaving it as a bare string, so the resulting Turtle emits
`prov:atLocation <https://...>` and validates cleanly against PROV-O's own constraints.
