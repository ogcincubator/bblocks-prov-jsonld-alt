
# W3C PROV-N (Model)

`ogc.ogc-utils.prov.w3c-prov-n` *v0.1*

The PROV Notation (PROV-N): a human-readable, non-XML/non-JSON textual notation for the W3C PROV data model, primarily used in specifications and diagnostics. A profile of the W3C PROV Representation Base.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

# W3C PROV-N

PROV-N is a textual, human-readable notation for PROV-DM instances. It has no JSON Schema of its
own (see the `ogc.ogc-utils.prov.w3c-prov-base` (W3C PROV Representation Base) for why); this block exists only to
register PROV-N as a first-class representation profile, with an example for cross-reference and
round-trip testing against the other profiles via the `prov` library's PROV-N parser/serializer.

## Examples

### A minimal CWL-style run (activity, plan-qualified and plain association, generation)
#### provn
```provn
document
  prefix ex <https://example.org/cwlprov/>

  entity(ex:plan/main)
  activity(ex:activity/step1, 2024-01-01T00:00:00+00:00, 2024-01-01T00:01:00+00:00)
  agent(ex:engine/cwltool, [prov:type='prov:SoftwareAgent'])
  wasAssociatedWith(ex:activity/step1, ex:engine/cwltool, ex:plan/main)
  wasAssociatedWith(ex:activity/step1, ex:engine/cwltool, -)
  entity(ex:data/output.txt)
  wasGeneratedBy(ex:data/output.txt, ex:activity/step1, -)
endDocument

```


### A real-world cwltool provenance run, as used in the OGC API - Processes Provenance Extension (https://docs.ogc.org/DRAFTS/26-038.html), re-serialized from the extension's job_prov.json PROV-JSON fixture with the `prov` library to guarantee it is byte-for-byte the same document as the other profiles' "ogcapi-processes-job" examples
#### provn
```provn
document
  prefix wfprov <http://purl.org/wf4ever/wfprov#>
  prefix wfdesc <http://purl.org/wf4ever/wfdesc#>
  prefix cwlprov <https://w3id.org/cwl/prov#>
  prefix foaf <http://xmlns.com/foaf/0.1/>
  prefix schema <http://schema.org/>
  prefix orcid <https://orcid.org/>
  prefix id <urn:uuid:>
  prefix data <urn:hash::sha1:>
  prefix sha256 <nih:sha-256;>
  prefix researchobject <arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/>
  prefix metadata <arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/metadata/>
  prefix provenance <arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/metadata/provenance/>
  prefix wf <arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/workflow/packed.cwl#>
  prefix input <arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/workflow/primary-job.json#>
  prefix doi <https://doi.org/>
  prefix wf4ever <http://purl.org/wf4ever/wf4ever#>
  prefix loc0 <https://hirondelle.crim.ca/>
  prefix loc1 <https://github.com/crim-ca/>
  prefix loc2 <http://pavics-weaver.readthedocs.org/en/>
  prefix loc3 <https://hirondelle.crim.ca/weaver/processes/EchoProcess/jobs/>
  prefix loc4 <https://hirondelle.crim.ca/weaver/processes/>
  
  agent(id:dc49c9ee-a913-4e5c-b89a-2201af36af9c)
  agent(id:dc49c9ee-a913-4e5c-b89a-2201af36af9c, [prov:type='foaf:OnlineAccount', prov:location='loc0:weaver', cwlprov:hostname="hirondelle.crim.ca"])
  agent(id:dc49c9ee-a913-4e5c-b89a-2201af36af9c, [prov:type='foaf:OnlineAccount', prov:label="weaver-worker@crim-ca/weaver:6.9.0-dev2", foaf:accountName="weaver-worker@crim-ca/weaver:6.9.0-dev2"])
  agent(id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990, [prov:type='prov:SoftwareAgent', prov:type='schema:SoftwareApplication', prov:label="weaver-worker@crim-ca/weaver:6.9.0-dev2", foaf:name="weaver-worker@crim-ca/weaver:6.9.0-dev2", foaf:account='id:dc49c9ee-a913-4e5c-b89a-2201af36af9c', schema:name="weaver-worker@crim-ca/weaver:6.9.0-dev2"])
  agent(id:d57aaff6-a93f-4927-a2d8-112beb358d4d, [prov:type='prov:SoftwareAgent', prov:type='wfprov:WorkflowEngine', prov:label="cwltool 3.1.20260108082145"])
  agent(data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067, [prov:generalEntity='data:_644e201526525f62152815a76a2dc773450f3dd9', prov:specificEntity='doi:_10.5281_zenodo.14210717', prov:type='prov:SoftwareAgent', prov:location='loc0:weaver', prov:label="crim-ca/weaver:6.9.0-dev2", prov:label="Weaver is an Execution Management Service (EMS) that allows the execution of workflows chaining various applications and Web Processing Services (WPS) inputs and outputs. Remote execution is deferred by the EMS to an Application Deployment and Execution Service (ADES), as defined by Common Workflow Language (CWL) configurations."])
  actedOnBehalfOf(id:dc49c9ee-a913-4e5c-b89a-2201af36af9c, id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990, -)
  actedOnBehalfOf(data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067, id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990, -)
  wasStartedBy(id:d57aaff6-a93f-4927-a2d8-112beb358d4d, -, id:dc49c9ee-a913-4e5c-b89a-2201af36af9c, 2026-01-15T16:46:10.775855)
  wasStartedBy(id:_53f5a04e-b531-466d-81be-62c34a1431ba, -, id:d57aaff6-a93f-4927-a2d8-112beb358d4d, 2026-01-15T16:46:10.775984)
  wasStartedBy(id:_53f5a04e-b531-466d-81be-62c34a1431ba, data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067, -, -)
  wasStartedBy(id:d57aaff6-a93f-4927-a2d8-112beb358d4d, id:_53f5a04e-b531-466d-81be-62c34a1431ba, -, 2026-01-15T16:45:56.964000+00:00)
  activity(id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:10.775907, -, [prov:type='wfprov:WorkflowRun', prov:label="Run of workflow/packed.cwl#main"])
  wasAssociatedWith(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:d57aaff6-a93f-4927-a2d8-112beb358d4d, wf:main)
  entity(data:_644e201526525f62152815a76a2dc773450f3dd9, [prov:type='prov:PrimarySource', prov:label="Source code repository", prov:location='loc1:weaver'])
  entity(data:_3102f6d7a018ebae572f457d711ed7e1e7a11bc2, [prov:type='prov:Organization', foaf:name="Computer Research Institute of Montréal", schema:name="Computer Research Institute of Montréal"])
  entity(data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0, [foaf:name="crim-ca/weaver", schema:name="crim-ca/weaver", prov:location='loc2:latest', prov:type='prov:Organization', prov:label="Server Provider"])
  entity(id:_53f5a04e-b531-466d-81be-62c34a1431ba, [prov:type='wfdesc:ProcessRun', prov:location='loc3:53f5a04e-b531-466d-81be-62c34a1431ba', prov:label="Job Information"])
  entity(data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess, [prov:type='wfdesc:Process', prov:location='loc4:EchoProcess', prov:label="Process Description"])
  entity(wf:main, [prov:type='wfdesc:Process', prov:type='prov:Plan', prov:label="Prospective provenance"])
  entity(data:_0cf60d40470fde378076afacf5812f961208a018, [prov:type='wfprov:Artifact', prov:value="Value2"])
  entity(data:_0cf60d40470fde378076afacf5812f961208a018, [prov:type='wfprov:Artifact', prov:value="Value2"])
  entity(data:_0cf60d40470fde378076afacf5812f961208a018, [prov:type='wfprov:Artifact', prov:value="Value2"])
  entity(id:cb4c5d07-5b7e-435f-882c-afe14e061f4b, [prov:value="10.3" %% xsd:double])
  entity(data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72, [prov:type='wfprov:Artifact', prov:value="2021-03-06T07:21:00"])
  entity(data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72, [prov:type='wfprov:Artifact', prov:value="2021-03-06T07:21:00"])
  entity(data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72, [prov:type='wfprov:Artifact', prov:value="2021-03-06T07:21:00"])
  entity(id:f01a7e80-f451-4047-93c0-587666a9847a, [prov:value="3.14159" %% xsd:double])
  entity(id:a19d9289-ab50-4d85-a241-4ef9a0e36deb, [prov:value=1])
  entity(id:_5e4614e1-101d-4be2-8b66-24f770b3435f, [prov:value=2])
  entity(id:a45ad975-3387-4b7c-ac1c-a268c65927d1, [prov:value=3])
  entity(id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f, [prov:value=4])
  entity(id:b4c63361-5926-4b48-be43-df94727a79da, [prov:value=5])
  entity(id:a68017f5-e2f6-441c-b4ad-cf94dec801d7, [prov:value=6])
  entity(id:c68b1b94-7f88-4cda-87da-f5e68beabe42, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c, [prov:type='wfprov:Artifact'])
  entity(data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c, [prov:type='wfprov:Artifact'])
  entity(id:_5f78096f-fce2-49b1-aa6d-941927d15dcc, [prov:type='wfprov:Artifact', prov:type='wf4ever:File'])
  entity(data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb, [prov:type='wfprov:Artifact'])
  entity(data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb, [prov:type='wfprov:Artifact'])
  entity(id:f0020803-854b-4bd3-a70a-f6317d3a6524, [prov:type='wfprov:Artifact', prov:type='wf4ever:File'])
  entity(data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5, [prov:type='wfprov:Artifact'])
  entity(data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5, [prov:type='wfprov:Artifact'])
  entity(id:_6e88c002-b8f6-488e-977f-21ad51073fc6, [prov:type='wfprov:Artifact', prov:type='wf4ever:File'])
  entity(id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d, [prov:type='wfprov:Artifact'])
  entity(data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d, [prov:type='wfprov:Artifact'])
  entity(id:d4ac4ab8-25a3-4412-82b6-07b92da98795, [prov:type='wfprov:Artifact', prov:type='wf4ever:File'])
  entity(data:ec3fe43f2db3829507e574b5b9b1b84547d48f19, [prov:type='wfprov:Artifact'])
  entity(data:ec3fe43f2db3829507e574b5b9b1b84547d48f19, [prov:type='wfprov:Artifact'])
  entity(id:c790f3f7-ac11-4d13-9c71-4d68c73ed040, [prov:type='wfprov:Artifact', prov:type='wf4ever:File'])
  entity(data:_795e8291ebb709a1bc71824449570f94f082a02b, [prov:type='wfprov:Artifact'])
  entity(data:_795e8291ebb709a1bc71824449570f94f082a02b, [prov:type='wfprov:Artifact'])
  entity(id:_6815d3c5-fa14-4153-befe-a5fddc285b06, [prov:type='wfprov:Artifact', prov:type='wf4ever:File'])
  entity(id:_88e9a099-e5d4-45f9-8402-c8082168a6f0, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(data:_3f88b16b3b80316d30a93bc4035da306170884e2, [prov:type='wfprov:Artifact'])
  entity(data:_3f88b16b3b80316d30a93bc4035da306170884e2, [prov:type='wfprov:Artifact'])
  entity(id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63, [prov:type='wfprov:Artifact', prov:type='wf4ever:File'])
  entity(id:fc017dcf-09ec-4cbf-81ac-741b5a61b482, [prov:value="10.3" %% xsd:double])
  entity(id:_0df32fa2-e262-458f-b1df-5e749c1b19f4, [prov:value="3.14159" %% xsd:double])
  entity(id:_5226c081-e3dc-4963-987b-92142bd75102, [prov:value=1])
  entity(id:f30572d8-60e4-4221-80a7-cb76e1007e9a, [prov:value=2])
  entity(id:a1aa3cbf-8435-4f94-aeb6-110922551843, [prov:value=3])
  entity(id:_2a95bd87-116b-42f4-8525-428de8743778, [prov:value=4])
  entity(id:bde07acc-95a9-46f6-be09-6467fa7bd8b8, [prov:value=5])
  entity(id:_6d234b31-69fb-4949-b096-924f234097a1, [prov:value=6])
  entity(id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(id:_109d6043-7fad-428f-a563-a99a4ebd6dda, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="input", cwlprov:nameroot="input", cwlprov:nameext=""])
  entity(id:_5ec5c130-692c-48d5-9cef-be41cec00d11, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="input_9i61gfqe", cwlprov:nameroot="input_9i61gfqe", cwlprov:nameext=""])
  entity(id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="input_50x5752r", cwlprov:nameroot="input_50x5752r", cwlprov:nameext=""])
  entity(id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(id:_160a1cd9-6384-4828-b627-a02e478365fb, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="input__cdpaqkt", cwlprov:nameroot="input__cdpaqkt", cwlprov:nameext=""])
  entity(id:ef9384d4-880f-4398-9e10-1bce1d54e51e, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="ew-hh.tiff", cwlprov:nameroot="ew-hh", cwlprov:nameext=".tiff"])
  entity(id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="input_9mob2l0c", cwlprov:nameroot="input_9mob2l0c", cwlprov:nameext=""])
  entity(id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(id:fbb085ae-d3ad-4639-a448-b01188f1ce9f, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="GetFeature.json", cwlprov:nameroot="GetFeature", cwlprov:nameext=".json"])
  entity(id:_5a1aa540-dfb8-46d5-8391-0b59b865747f, [prov:value="10.3" %% xsd:double])
  entity(id:_0aebe062-805e-4853-9d80-dbc5107a8bdb, [prov:value="3.14159" %% xsd:double])
  entity(id:_6a99e0ba-c671-4471-aa33-4cc523e0f428, [prov:value=1])
  entity(id:_64c45605-d8a9-4a56-929d-47dcad5543f1, [prov:value=2])
  entity(id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f, [prov:value=3])
  entity(id:f55d0d44-4cb4-4cd2-a336-7bac9e265583, [prov:value=4])
  entity(id:c8dbab29-6641-40d9-b5c1-626872f5337d, [prov:value=5])
  entity(id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150, [prov:value=6])
  entity(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(id:a326f7d5-60b5-4b9d-802f-58f2411c993e, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(id:_96f693e2-3eac-4a04-8887-7285b7605f49, [prov:type='wfprov:Artifact', prov:type='prov:Collection'])
  entity(data:da39a3ee5e6b4b0d3255bfef95601890afd80709, [prov:type='wfprov:Artifact'])
  entity(id:a9b3da73-190e-4a3a-affb-a12396f0eac3, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="stderr.log", cwlprov:nameroot="stderr", cwlprov:nameext=".log"])
  entity(data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc, [prov:type='wfprov:Artifact'])
  entity(id:e66cf62a-753e-459e-b2f4-06f99396ca08, [prov:type='wfprov:Artifact', prov:type='wf4ever:File', cwlprov:basename="stdout.log", cwlprov:nameroot="stdout", cwlprov:nameext=".log"])
  wasDerivedFrom(data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067, data:_644e201526525f62152815a76a2dc773450f3dd9, -, -, -, [prov:type='prov:PrimarySource'])
  wasDerivedFrom(id:dc49c9ee-a913-4e5c-b89a-2201af36af9c, data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067, -, -, -)
  wasDerivedFrom(data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0, data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067, -, -, -)
  specializationOf(data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067, id:dc49c9ee-a913-4e5c-b89a-2201af36af9c)
  specializationOf(id:d57aaff6-a93f-4927-a2d8-112beb358d4d, id:_53f5a04e-b531-466d-81be-62c34a1431ba)
  specializationOf(id:_5f78096f-fce2-49b1-aa6d-941927d15dcc, data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c)
  specializationOf(id:f0020803-854b-4bd3-a70a-f6317d3a6524, data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb)
  specializationOf(id:_6e88c002-b8f6-488e-977f-21ad51073fc6, data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5)
  specializationOf(id:d4ac4ab8-25a3-4412-82b6-07b92da98795, data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d)
  specializationOf(id:c790f3f7-ac11-4d13-9c71-4d68c73ed040, data:ec3fe43f2db3829507e574b5b9b1b84547d48f19)
  specializationOf(id:_6815d3c5-fa14-4153-befe-a5fddc285b06, data:_795e8291ebb709a1bc71824449570f94f082a02b)
  specializationOf(id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63, data:_3f88b16b3b80316d30a93bc4035da306170884e2)
  specializationOf(id:_109d6043-7fad-428f-a563-a99a4ebd6dda, data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c)
  specializationOf(id:_5ec5c130-692c-48d5-9cef-be41cec00d11, data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb)
  specializationOf(id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304, data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5)
  specializationOf(id:_160a1cd9-6384-4828-b627-a02e478365fb, data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d)
  specializationOf(id:ef9384d4-880f-4398-9e10-1bce1d54e51e, data:ec3fe43f2db3829507e574b5b9b1b84547d48f19)
  specializationOf(id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9, data:_795e8291ebb709a1bc71824449570f94f082a02b)
  specializationOf(id:fbb085ae-d3ad-4639-a448-b01188f1ce9f, data:_3f88b16b3b80316d30a93bc4035da306170884e2)
  specializationOf(id:a9b3da73-190e-4a3a-affb-a12396f0eac3, data:da39a3ee5e6b4b0d3255bfef95601890afd80709)
  specializationOf(id:e66cf62a-753e-459e-b2f4-06f99396ca08, data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc)
  wasAttributedTo(data:_3102f6d7a018ebae572f457d711ed7e1e7a11bc2, data:_644e201526525f62152815a76a2dc773450f3dd9)
  wasAttributedTo(data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0, data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067)
  alternateOf(id:d57aaff6-a93f-4927-a2d8-112beb358d4d, id:_53f5a04e-b531-466d-81be-62c34a1431ba)
  wasGeneratedBy(id:_53f5a04e-b531-466d-81be-62c34a1431ba, data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess, -)
  wasGeneratedBy(data:_0cf60d40470fde378076afacf5812f961208a018, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_stringOutput'])
  wasGeneratedBy(id:_5a1aa540-dfb8-46d5-8391-0b59b865747f, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_measureOutput'])
  wasGeneratedBy(data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_dateOutput'])
  wasGeneratedBy(id:_0aebe062-805e-4853-9d80-dbc5107a8bdb, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_doubleOutput'])
  wasGeneratedBy(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_arrayOutput'])
  wasGeneratedBy(id:_109d6043-7fad-428f-a563-a99a4ebd6dda, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_complexObjectOutput'])
  wasGeneratedBy(id:a326f7d5-60b5-4b9d-802f-58f2411c993e, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_geometryOutput'])
  wasGeneratedBy(id:_160a1cd9-6384-4828-b627-a02e478365fb, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_boundingBoxOutput'])
  wasGeneratedBy(id:_96f693e2-3eac-4a04-8887-7285b7605f49, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_imagesOutput'])
  wasGeneratedBy(id:fbb085ae-d3ad-4639-a448-b01188f1ce9f, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_featureCollectionOutput'])
  wasGeneratedBy(id:a9b3da73-190e-4a3a-affb-a12396f0eac3, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_a5f8bd13-1ab3-4633-9219-810292b59056'])
  wasGeneratedBy(id:e66cf62a-753e-459e-b2f4-06f99396ca08, id:_53f5a04e-b531-466d-81be-62c34a1431ba, 2026-01-15T16:46:11.414795, [prov:role='wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_b62df1f5-a3e7-412c-bdc0-0451aa8a4d93'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, data:_0cf60d40470fde378076afacf5812f961208a018, 2026-01-15T16:46:10.807817, [prov:role='wf:main_stringInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:cb4c5d07-5b7e-435f-882c-afe14e061f4b, 2026-01-15T16:46:10.807975, [prov:role='wf:main_measureInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72, 2026-01-15T16:46:10.808789, [prov:role='wf:main_dateInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:f01a7e80-f451-4047-93c0-587666a9847a, 2026-01-15T16:46:10.808944, [prov:role='wf:main_doubleInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:c68b1b94-7f88-4cda-87da-f5e68beabe42, 2026-01-15T16:46:10.809545, [prov:role='wf:main_arrayInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_5f78096f-fce2-49b1-aa6d-941927d15dcc, 2026-01-15T16:46:10.810650, [prov:role='wf:main_complexObjectInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3, 2026-01-15T16:46:10.812817, [prov:role='wf:main_geometryInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:d4ac4ab8-25a3-4412-82b6-07b92da98795, 2026-01-15T16:46:10.813646, [prov:role='wf:main_boundingBoxInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_88e9a099-e5d4-45f9-8402-c8082168a6f0, 2026-01-15T16:46:11.100961, [prov:role='wf:main_imagesInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63, 2026-01-15T16:46:11.101847, [prov:role='wf:main_featureCollectionInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, data:_0cf60d40470fde378076afacf5812f961208a018, 2026-01-15T16:46:11.105949, [prov:role='wf:main_EchoProcess_stringInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:fc017dcf-09ec-4cbf-81ac-741b5a61b482, 2026-01-15T16:46:11.106052, [prov:role='wf:main_EchoProcess_measureInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72, 2026-01-15T16:46:11.106625, [prov:role='wf:main_EchoProcess_dateInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_0df32fa2-e262-458f-b1df-5e749c1b19f4, 2026-01-15T16:46:11.106731, [prov:role='wf:main_EchoProcess_doubleInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, 2026-01-15T16:46:11.107097, [prov:role='wf:main_EchoProcess_arrayInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_109d6043-7fad-428f-a563-a99a4ebd6dda, 2026-01-15T16:46:11.107662, [prov:role='wf:main_EchoProcess_complexObjectInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823, 2026-01-15T16:46:11.108679, [prov:role='wf:main_EchoProcess_geometryInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:_160a1cd9-6384-4828-b627-a02e478365fb, 2026-01-15T16:46:11.109174, [prov:role='wf:main_EchoProcess_boundingBoxInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5, 2026-01-15T16:46:11.401124, [prov:role='wf:main_EchoProcess_imagesInput'])
  used(id:_53f5a04e-b531-466d-81be-62c34a1431ba, id:fbb085ae-d3ad-4639-a448-b01188f1ce9f, 2026-01-15T16:46:11.401851, [prov:role='wf:main_EchoProcess_featureCollectionInput'])
  hadMember(id:c68b1b94-7f88-4cda-87da-f5e68beabe42, id:a19d9289-ab50-4d85-a241-4ef9a0e36deb)
  hadMember(id:c68b1b94-7f88-4cda-87da-f5e68beabe42, id:_5e4614e1-101d-4be2-8b66-24f770b3435f)
  hadMember(id:c68b1b94-7f88-4cda-87da-f5e68beabe42, id:a45ad975-3387-4b7c-ac1c-a268c65927d1)
  hadMember(id:c68b1b94-7f88-4cda-87da-f5e68beabe42, id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f)
  hadMember(id:c68b1b94-7f88-4cda-87da-f5e68beabe42, id:b4c63361-5926-4b48-be43-df94727a79da)
  hadMember(id:c68b1b94-7f88-4cda-87da-f5e68beabe42, id:a68017f5-e2f6-441c-b4ad-cf94dec801d7)
  hadMember(id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3, id:f0020803-854b-4bd3-a70a-f6317d3a6524)
  hadMember(id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3, id:_6e88c002-b8f6-488e-977f-21ad51073fc6)
  hadMember(id:_88e9a099-e5d4-45f9-8402-c8082168a6f0, id:c790f3f7-ac11-4d13-9c71-4d68c73ed040)
  hadMember(id:_88e9a099-e5d4-45f9-8402-c8082168a6f0, id:_6815d3c5-fa14-4153-befe-a5fddc285b06)
  hadMember(id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, id:_5226c081-e3dc-4963-987b-92142bd75102)
  hadMember(id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, id:f30572d8-60e4-4221-80a7-cb76e1007e9a)
  hadMember(id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, id:a1aa3cbf-8435-4f94-aeb6-110922551843)
  hadMember(id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, id:_2a95bd87-116b-42f4-8525-428de8743778)
  hadMember(id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, id:bde07acc-95a9-46f6-be09-6467fa7bd8b8)
  hadMember(id:_541c0738-ac5c-4a35-b592-a3cbc87246f1, id:_6d234b31-69fb-4949-b096-924f234097a1)
  hadMember(id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823, id:_5ec5c130-692c-48d5-9cef-be41cec00d11)
  hadMember(id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823, id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304)
  hadMember(id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5, id:ef9384d4-880f-4398-9e10-1bce1d54e51e)
  hadMember(id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5, id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9)
  hadMember(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, id:_6a99e0ba-c671-4471-aa33-4cc523e0f428)
  hadMember(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, id:_64c45605-d8a9-4a56-929d-47dcad5543f1)
  hadMember(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f)
  hadMember(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, id:f55d0d44-4cb4-4cd2-a336-7bac9e265583)
  hadMember(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, id:c8dbab29-6641-40d9-b5c1-626872f5337d)
  hadMember(id:_79e5fa0b-4998-46da-bbe8-920533c7940b, id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150)
  hadMember(id:a326f7d5-60b5-4b9d-802f-58f2411c993e, id:_5ec5c130-692c-48d5-9cef-be41cec00d11)
  hadMember(id:a326f7d5-60b5-4b9d-802f-58f2411c993e, id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304)
  hadMember(id:_96f693e2-3eac-4a04-8887-7285b7605f49, id:ef9384d4-880f-4398-9e10-1bce1d54e51e)
  hadMember(id:_96f693e2-3eac-4a04-8887-7285b7605f49, id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9)
  wasEndedBy(id:_53f5a04e-b531-466d-81be-62c34a1431ba, -, id:d57aaff6-a93f-4927-a2d8-112beb358d4d, 2026-01-15T16:46:11.419318)
endDocument
```

## Sources

* [PROV-N: The Provenance Notation](https://www.w3.org/TR/prov-n/)
* [OGC API - Processes - Part 5: Provenance (registers `text/provenance-notation` for PROV-N)](https://docs.ogc.org/DRAFTS/26-038.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-prov-jsonld-alt](https://github.com/ogcincubator/bblocks-prov-jsonld-alt)
* Path: `_sources/prov/w3c-prov-n`

