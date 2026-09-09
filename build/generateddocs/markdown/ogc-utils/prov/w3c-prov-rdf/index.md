
# W3C PROV-O / RDF (Model)

`ogc.ogc-utils.prov.w3c-prov-rdf` *v0.1*

The RDF binding of the W3C PROV data model via the PROV Ontology (PROV-O), serializable as Turtle, N-Triples, RDF/XML, N-Quads, TriG, etc. A profile of the W3C PROV Representation Base.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

# W3C PROV-O / RDF

PROV-O maps every PROV-DM concept directly onto RDF classes/properties, so this block is an
RDF-only block (see [rdf-only.md](https://github.com/opengeospatial/bblocks-postprocess) pattern):
no JSON Schema, `ontology` points at the PROV-O document, and the example below is Turtle.

The example illustrates a nuance also relevant to `ogc.ogc-utils.prov.w3c-prov-jsonld` (W3C PROV-JSONLD):
an `Association` qualified with extra attributes (here, `prov:hadPlan`) is reified as a blank node
(`prov:qualifiedAssociation`) *and*, separately, a plain `prov:wasAssociatedWith` shortcut triple is
still needed on the activity for tools that only read the shortcut property.

## Note on the OGC API - Processes example's `prov:atLocation` values

The source PROV-JSON fixture behind `example-ogcapi-processes-job` declares its `prov:location`
values as plain untyped strings (e.g. `"https://hirondelle.crim.ca/weaver"`), which `prov` would
by default carry through as RDF literals. Turtle's `sh:nodeKind sh:IRI` / `prov:Location`-typed
blank-node requirement (from the imported `cross-domain-model` SHACL shapes) expects
`prov:atLocation` to be a resource, not a literal, so this example's regeneration script
re-types each such value as a proper IRI (splitting the URI into a namespace + local part and
registering it as a `QualifiedName`) rather than leaving it as a bare string, so the resulting
Turtle emits `prov:atLocation <https://...>` and validates cleanly.

## Examples

### A minimal CWL-style run (activity, plan-qualified and plain association, generation)
#### turtle
```turtle
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://example.org/cwlprov/data/output.txt> a prov:Entity ;
    prov:wasGeneratedBy <https://example.org/cwlprov/activity/step1> .

<https://example.org/cwlprov/activity/step1> a prov:Activity ;
    prov:endedAtTime "2024-01-01T00:01:00+00:00"^^xsd:dateTime ;
    prov:qualifiedAssociation [ a prov:Association ;
            prov:agent <https://example.org/cwlprov/engine/cwltool> ;
            prov:hadPlan <https://example.org/cwlprov/plan/main> ] ;
    prov:startedAtTime "2024-01-01T00:00:00+00:00"^^xsd:dateTime ;
    prov:wasAssociatedWith <https://example.org/cwlprov/engine/cwltool> .

<https://example.org/cwlprov/plan/main> a prov:Entity .

<https://example.org/cwlprov/engine/cwltool> a prov:Agent,
        prov:SoftwareAgent .

```


### A real-world cwltool provenance run, as used in the OGC API - Processes Provenance Extension (https://docs.ogc.org/DRAFTS/26-038.html), re-serialized from the extension's job_prov.json PROV-JSON fixture with the `prov` library to guarantee it is byte-for-byte the same document as the other profiles' "ogcapi-processes-job" examples
#### turtle
```turtle
@prefix cwlprov: <https://w3id.org/cwl/prov#> .
@prefix data: <urn:hash::sha1:> .
@prefix doi: <https://doi.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix id: <urn:uuid:> .
@prefix loc0: <https://hirondelle.crim.ca/> .
@prefix loc1: <https://github.com/crim-ca/> .
@prefix loc2: <http://pavics-weaver.readthedocs.org/en/> .
@prefix loc3: <https://hirondelle.crim.ca/weaver/processes/EchoProcess/jobs/> .
@prefix loc4: <https://hirondelle.crim.ca/weaver/processes/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema1: <http://schema.org/> .
@prefix wf: <arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/workflow/packed.cwl#> .
@prefix wf4ever: <http://purl.org/wf4ever/wf4ever#> .
@prefix wfdesc: <http://purl.org/wf4ever/wfdesc#> .
@prefix wfprov: <http://purl.org/wf4ever/wfprov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

data:_3102f6d7a018ebae572f457d711ed7e1e7a11bc2 a prov:Entity,
        prov:Organization ;
    schema1:name "Computer Research Institute of Montréal" ;
    prov:wasAttributedTo data:_644e201526525f62152815a76a2dc773450f3dd9 ;
    foaf:name "Computer Research Institute of Montréal" .

data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0 a prov:Entity,
        prov:Organization ;
    rdfs:label "Server Provider" ;
    schema1:name "crim-ca/weaver" ;
    prov:atLocation loc2:latest ;
    prov:wasAttributedTo data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 ;
    prov:wasDerivedFrom data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 ;
    foaf:name "crim-ca/weaver" .

id:_0aebe062-805e-4853-9d80-dbc5107a8bdb a prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_doubleOutput ] ;
    prov:value "3.14159"^^xsd:double .

id:_5a1aa540-dfb8-46d5-8391-0b59b865747f a prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_measureOutput ] ;
    prov:value "10.3"^^xsd:double .

id:_79e5fa0b-4998-46da-bbe8-920533c7940b a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_64c45605-d8a9-4a56-929d-47dcad5543f1,
        id:_6a99e0ba-c671-4471-aa33-4cc523e0f428,
        id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150,
        id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f,
        id:c8dbab29-6641-40d9-b5c1-626872f5337d,
        id:f55d0d44-4cb4-4cd2-a336-7bac9e265583 ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_arrayOutput ] .

id:_96f693e2-3eac-4a04-8887-7285b7605f49 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9,
        id:ef9384d4-880f-4398-9e10-1bce1d54e51e ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_imagesOutput ] .

id:a326f7d5-60b5-4b9d-802f-58f2411c993e a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_5ec5c130-692c-48d5-9cef-be41cec00d11,
        id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304 ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_geometryOutput ] .

id:a9b3da73-190e-4a3a-affb-a12396f0eac3 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_a5f8bd13-1ab3-4633-9219-810292b59056 ] ;
    prov:specializationOf data:da39a3ee5e6b4b0d3255bfef95601890afd80709 ;
    cwlprov:basename "stderr.log" ;
    cwlprov:nameext ".log" ;
    cwlprov:nameroot "stderr" .

id:e66cf62a-753e-459e-b2f4-06f99396ca08 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_b62df1f5-a3e7-412c-bdc0-0451aa8a4d93 ] ;
    prov:specializationOf data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc ;
    cwlprov:basename "stdout.log" ;
    cwlprov:nameext ".log" ;
    cwlprov:nameroot "stdout" .

wf:main a wfdesc:Process,
        prov:Entity,
        prov:Plan ;
    rdfs:label "Prospective provenance" .

data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess a wfdesc:Process,
        prov:Entity ;
    rdfs:label "Process Description" ;
    prov:atLocation loc4:EchoProcess .

data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc a wfprov:Artifact,
        prov:Entity .

data:da39a3ee5e6b4b0d3255bfef95601890afd80709 a wfprov:Artifact,
        prov:Entity .

id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f a prov:Entity ;
    prov:value "4"^^xsd:int .

id:_0df32fa2-e262-458f-b1df-5e749c1b19f4 a prov:Entity ;
    prov:value "3.14159"^^xsd:double .

id:_109d6043-7fad-428f-a563-a99a4ebd6dda a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_complexObjectOutput ] ;
    prov:specializationOf data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c ;
    cwlprov:basename "input" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input" .

id:_160a1cd9-6384-4828-b627-a02e478365fb a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_boundingBoxOutput ] ;
    prov:specializationOf data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d ;
    cwlprov:basename "input__cdpaqkt" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input__cdpaqkt" .

id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_5ec5c130-692c-48d5-9cef-be41cec00d11,
        id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304 .

id:_2a95bd87-116b-42f4-8525-428de8743778 a prov:Entity ;
    prov:value "4"^^xsd:int .

id:_5226c081-e3dc-4963-987b-92142bd75102 a prov:Entity ;
    prov:value "1"^^xsd:int .

id:_541c0738-ac5c-4a35-b592-a3cbc87246f1 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_2a95bd87-116b-42f4-8525-428de8743778,
        id:_5226c081-e3dc-4963-987b-92142bd75102,
        id:_6d234b31-69fb-4949-b096-924f234097a1,
        id:a1aa3cbf-8435-4f94-aeb6-110922551843,
        id:bde07acc-95a9-46f6-be09-6467fa7bd8b8,
        id:f30572d8-60e4-4221-80a7-cb76e1007e9a .

id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:_3f88b16b3b80316d30a93bc4035da306170884e2 .

id:_5e4614e1-101d-4be2-8b66-24f770b3435f a prov:Entity ;
    prov:value "2"^^xsd:int .

id:_5f78096f-fce2-49b1-aa6d-941927d15dcc a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c .

id:_64c45605-d8a9-4a56-929d-47dcad5543f1 a prov:Entity ;
    prov:value "2"^^xsd:int .

id:_6815d3c5-fa14-4153-befe-a5fddc285b06 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:_795e8291ebb709a1bc71824449570f94f082a02b .

id:_6a99e0ba-c671-4471-aa33-4cc523e0f428 a prov:Entity ;
    prov:value "1"^^xsd:int .

id:_6d234b31-69fb-4949-b096-924f234097a1 a prov:Entity ;
    prov:value "6"^^xsd:int .

id:_6e88c002-b8f6-488e-977f-21ad51073fc6 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5 .

id:_88e9a099-e5d4-45f9-8402-c8082168a6f0 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_6815d3c5-fa14-4153-befe-a5fddc285b06,
        id:c790f3f7-ac11-4d13-9c71-4d68c73ed040 .

id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_6e88c002-b8f6-488e-977f-21ad51073fc6,
        id:f0020803-854b-4bd3-a70a-f6317d3a6524 .

id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150 a prov:Entity ;
    prov:value "6"^^xsd:int .

id:a19d9289-ab50-4d85-a241-4ef9a0e36deb a prov:Entity ;
    prov:value "1"^^xsd:int .

id:a1aa3cbf-8435-4f94-aeb6-110922551843 a prov:Entity ;
    prov:value "3"^^xsd:int .

id:a45ad975-3387-4b7c-ac1c-a268c65927d1 a prov:Entity ;
    prov:value "3"^^xsd:int .

id:a68017f5-e2f6-441c-b4ad-cf94dec801d7 a prov:Entity ;
    prov:value "6"^^xsd:int .

id:b4c63361-5926-4b48-be43-df94727a79da a prov:Entity ;
    prov:value "5"^^xsd:int .

id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f a prov:Entity ;
    prov:value "3"^^xsd:int .

id:bde07acc-95a9-46f6-be09-6467fa7bd8b8 a prov:Entity ;
    prov:value "5"^^xsd:int .

id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9,
        id:ef9384d4-880f-4398-9e10-1bce1d54e51e .

id:c68b1b94-7f88-4cda-87da-f5e68beabe42 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:hadMember id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f,
        id:_5e4614e1-101d-4be2-8b66-24f770b3435f,
        id:a19d9289-ab50-4d85-a241-4ef9a0e36deb,
        id:a45ad975-3387-4b7c-ac1c-a268c65927d1,
        id:a68017f5-e2f6-441c-b4ad-cf94dec801d7,
        id:b4c63361-5926-4b48-be43-df94727a79da .

id:c790f3f7-ac11-4d13-9c71-4d68c73ed040 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:ec3fe43f2db3829507e574b5b9b1b84547d48f19 .

id:c8dbab29-6641-40d9-b5c1-626872f5337d a prov:Entity ;
    prov:value "5"^^xsd:int .

id:cb4c5d07-5b7e-435f-882c-afe14e061f4b a prov:Entity ;
    prov:value "10.3"^^xsd:double .

id:d4ac4ab8-25a3-4412-82b6-07b92da98795 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d .

id:f0020803-854b-4bd3-a70a-f6317d3a6524 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb .

id:f01a7e80-f451-4047-93c0-587666a9847a a prov:Entity ;
    prov:value "3.14159"^^xsd:double .

id:f30572d8-60e4-4221-80a7-cb76e1007e9a a prov:Entity ;
    prov:value "2"^^xsd:int .

id:f55d0d44-4cb4-4cd2-a336-7bac9e265583 a prov:Entity ;
    prov:value "4"^^xsd:int .

id:fbb085ae-d3ad-4639-a448-b01188f1ce9f a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_featureCollectionOutput ] ;
    prov:specializationOf data:_3f88b16b3b80316d30a93bc4035da306170884e2 ;
    cwlprov:basename "GetFeature.json" ;
    cwlprov:nameext ".json" ;
    cwlprov:nameroot "GetFeature" .

id:fc017dcf-09ec-4cbf-81ac-741b5a61b482 a prov:Entity ;
    prov:value "10.3"^^xsd:double .

data:_0cf60d40470fde378076afacf5812f961208a018 a wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_stringOutput ] ;
    prov:value "Value2" .

data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c a wfprov:Artifact,
        prov:Entity .

data:_3f88b16b3b80316d30a93bc4035da306170884e2 a wfprov:Artifact,
        prov:Entity .

data:_795e8291ebb709a1bc71824449570f94f082a02b a wfprov:Artifact,
        prov:Entity .

data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5 a wfprov:Artifact,
        prov:Entity .

data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72 a wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_dateOutput ] ;
    prov:value "2021-03-06T07:21:00" .

data:ec3fe43f2db3829507e574b5b9b1b84547d48f19 a wfprov:Artifact,
        prov:Entity .

data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb a wfprov:Artifact,
        prov:Entity .

data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d a wfprov:Artifact,
        prov:Entity .

id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:_795e8291ebb709a1bc71824449570f94f082a02b ;
    cwlprov:basename "input_9mob2l0c" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input_9mob2l0c" .

id:_5ec5c130-692c-48d5-9cef-be41cec00d11 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb ;
    cwlprov:basename "input_9i61gfqe" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input_9i61gfqe" .

id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990 a schema1:SoftwareApplication,
        prov:Agent,
        prov:SoftwareAgent ;
    rdfs:label "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    schema1:name "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    foaf:account id:dc49c9ee-a913-4e5c-b89a-2201af36af9c ;
    foaf:name "weaver-worker@crim-ca/weaver:6.9.0-dev2" .

id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5 ;
    cwlprov:basename "input_50x5752r" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input_50x5752r" .

id:ef9384d4-880f-4398-9e10-1bce1d54e51e a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:specializationOf data:ec3fe43f2db3829507e574b5b9b1b84547d48f19 ;
    cwlprov:basename "ew-hh.tiff" ;
    cwlprov:nameext ".tiff" ;
    cwlprov:nameroot "ew-hh" .

data:_644e201526525f62152815a76a2dc773450f3dd9 a prov:Entity,
        prov:PrimarySource ;
    rdfs:label "Source code repository" ;
    prov:atLocation loc1:weaver .

id:d57aaff6-a93f-4927-a2d8-112beb358d4d a wfprov:WorkflowEngine,
        prov:Agent,
        prov:SoftwareAgent ;
    rdfs:label "cwltool 3.1.20260108082145" ;
    prov:alternateOf id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
    prov:qualifiedStart [ a prov:Start ;
            prov:atTime "2026-01-15T16:45:56.964000+00:00"^^xsd:dateTime ;
            prov:entity id:_53f5a04e-b531-466d-81be-62c34a1431ba ],
        [ a prov:Start ;
            prov:atTime "2026-01-15T16:46:10.775855"^^xsd:dateTime ;
            prov:hadActivity id:dc49c9ee-a913-4e5c-b89a-2201af36af9c ] ;
    prov:specializationOf id:_53f5a04e-b531-466d-81be-62c34a1431ba .

id:dc49c9ee-a913-4e5c-b89a-2201af36af9c a prov:Agent,
        foaf:OnlineAccount ;
    rdfs:label "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    prov:actedOnBehalfOf id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990 ;
    prov:atLocation loc0:weaver ;
    prov:wasDerivedFrom data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 ;
    foaf:accountName "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    cwlprov:hostname "hirondelle.crim.ca" .

data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 a prov:Agent,
        prov:SoftwareAgent ;
    rdfs:label "Weaver is an Execution Management Service (EMS) that allows the execution of workflows chaining various applications and Web Processing Services (WPS) inputs and outputs. Remote execution is deferred by the EMS to an Application Deployment and Execution Service (ADES), as defined by Common Workflow Language (CWL) configurations.",
        "crim-ca/weaver:6.9.0-dev2" ;
    prov:actedOnBehalfOf id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990 ;
    prov:atLocation loc0:weaver ;
    prov:generalEntity data:_644e201526525f62152815a76a2dc773450f3dd9 ;
    prov:qualifiedPrimarySource [ a prov:PrimarySource ;
            prov:entity data:_644e201526525f62152815a76a2dc773450f3dd9 ] ;
    prov:specializationOf id:dc49c9ee-a913-4e5c-b89a-2201af36af9c ;
    prov:specificEntity doi:_10.5281_zenodo.14210717 .

id:_53f5a04e-b531-466d-81be-62c34a1431ba a wfdesc:ProcessRun,
        wfprov:WorkflowRun,
        prov:Activity,
        prov:Entity ;
    rdfs:label "Job Information",
        "Run of workflow/packed.cwl#main" ;
    prov:atLocation loc3:53f5a04e-b531-466d-81be-62c34a1431ba ;
    prov:qualifiedAssociation [ a prov:Association ;
            prov:agent id:d57aaff6-a93f-4927-a2d8-112beb358d4d ;
            prov:hadPlan wf:main ] ;
    prov:qualifiedEnd [ a prov:End ;
            prov:atTime "2026-01-15T16:46:11.419318"^^xsd:dateTime ;
            prov:hadActivity id:d57aaff6-a93f-4927-a2d8-112beb358d4d ] ;
    prov:qualifiedStart [ a prov:Start ;
            prov:atTime "2026-01-15T16:46:10.775984"^^xsd:dateTime ;
            prov:hadActivity id:d57aaff6-a93f-4927-a2d8-112beb358d4d ] ;
    prov:qualifiedUsage [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.809545"^^xsd:dateTime ;
            prov:entity id:c68b1b94-7f88-4cda-87da-f5e68beabe42 ;
            prov:hadRole wf:main_arrayInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.106052"^^xsd:dateTime ;
            prov:entity id:fc017dcf-09ec-4cbf-81ac-741b5a61b482 ;
            prov:hadRole wf:main_EchoProcess_measureInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.810650"^^xsd:dateTime ;
            prov:entity id:_5f78096f-fce2-49b1-aa6d-941927d15dcc ;
            prov:hadRole wf:main_complexObjectInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.107097"^^xsd:dateTime ;
            prov:entity id:_541c0738-ac5c-4a35-b592-a3cbc87246f1 ;
            prov:hadRole wf:main_EchoProcess_arrayInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.812817"^^xsd:dateTime ;
            prov:entity id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3 ;
            prov:hadRole wf:main_geometryInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.101847"^^xsd:dateTime ;
            prov:entity id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63 ;
            prov:hadRole wf:main_featureCollectionInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.813646"^^xsd:dateTime ;
            prov:entity id:d4ac4ab8-25a3-4412-82b6-07b92da98795 ;
            prov:hadRole wf:main_boundingBoxInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.401124"^^xsd:dateTime ;
            prov:entity id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5 ;
            prov:hadRole wf:main_EchoProcess_imagesInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.105949"^^xsd:dateTime ;
            prov:entity data:_0cf60d40470fde378076afacf5812f961208a018 ;
            prov:hadRole wf:main_EchoProcess_stringInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.808944"^^xsd:dateTime ;
            prov:entity id:f01a7e80-f451-4047-93c0-587666a9847a ;
            prov:hadRole wf:main_doubleInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.807817"^^xsd:dateTime ;
            prov:entity data:_0cf60d40470fde378076afacf5812f961208a018 ;
            prov:hadRole wf:main_stringInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.106731"^^xsd:dateTime ;
            prov:entity id:_0df32fa2-e262-458f-b1df-5e749c1b19f4 ;
            prov:hadRole wf:main_EchoProcess_doubleInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.100961"^^xsd:dateTime ;
            prov:entity id:_88e9a099-e5d4-45f9-8402-c8082168a6f0 ;
            prov:hadRole wf:main_imagesInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.108679"^^xsd:dateTime ;
            prov:entity id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823 ;
            prov:hadRole wf:main_EchoProcess_geometryInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.808789"^^xsd:dateTime ;
            prov:entity data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72 ;
            prov:hadRole wf:main_dateInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.106625"^^xsd:dateTime ;
            prov:entity data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72 ;
            prov:hadRole wf:main_EchoProcess_dateInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.401851"^^xsd:dateTime ;
            prov:entity id:fbb085ae-d3ad-4639-a448-b01188f1ce9f ;
            prov:hadRole wf:main_EchoProcess_featureCollectionInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.107662"^^xsd:dateTime ;
            prov:entity id:_109d6043-7fad-428f-a563-a99a4ebd6dda ;
            prov:hadRole wf:main_EchoProcess_complexObjectInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.807975"^^xsd:dateTime ;
            prov:entity id:cb4c5d07-5b7e-435f-882c-afe14e061f4b ;
            prov:hadRole wf:main_measureInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.109174"^^xsd:dateTime ;
            prov:entity id:_160a1cd9-6384-4828-b627-a02e478365fb ;
            prov:hadRole wf:main_EchoProcess_boundingBoxInput ] ;
    prov:startedAtTime "2026-01-15T16:46:10.775907"^^xsd:dateTime ;
    prov:wasGeneratedBy data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess ;
    prov:wasStartedBy data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 .


```

## Sources

* [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)
* [OGC API - Processes - Part 5: Provenance (registers `text/turtle` for PROV-TURTLE and `application/n-triples` for PROV-NT)](https://docs.ogc.org/DRAFTS/26-038.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-prov-jsonld-alt](https://github.com/ogcincubator/bblocks-prov-jsonld-alt)
* Path: `_sources/prov/w3c-prov-rdf`

