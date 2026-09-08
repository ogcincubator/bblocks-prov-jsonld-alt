# PROV-XML

PROV-XML binds PROV-DM to XML using the schema referenced above. As with PROV-N, there is no JSON
Schema involved (see the [base block](bblocks://ogc.ogc-utils.prov.base)); the XSD is referenced
directly via `resources` (role `schema`) rather than duplicated locally.
