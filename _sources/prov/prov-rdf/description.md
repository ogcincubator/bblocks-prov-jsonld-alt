# PROV-O / RDF

PROV-O maps every PROV-DM concept directly onto RDF classes/properties, so this block is an
RDF-only block (see [rdf-only.md](https://github.com/opengeospatial/bblocks-postprocess) pattern):
no JSON Schema, `ontology` points at the PROV-O document, and the example below is Turtle.

The example illustrates a nuance also relevant to [PROV-JSONLD](bblocks://ogc.ogc-utils.prov.prov-jsonld):
an `Association` qualified with extra attributes (here, `prov:hadPlan`) is reified as a blank node
(`prov:qualifiedAssociation`) *and*, separately, a plain `prov:wasAssociatedWith` shortcut triple is
still needed on the activity for tools that only read the shortcut property.
