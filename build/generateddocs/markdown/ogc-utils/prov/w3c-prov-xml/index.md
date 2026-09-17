
# W3C PROV-XML (Model)

`ogc.ogc-utils.prov.w3c-prov-xml` *v0.1*

The PROV-XML serialization: an XML Schema binding of the W3C PROV data model. A profile of the W3C PROV Representation Base.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

# W3C PROV-XML

PROV-XML binds PROV-DM to XML using the schema referenced above. As with PROV-N, there is no JSON
Schema involved (see [`ogc.ogc-utils.prov.w3c-prov-base`](bblocks://ogc.ogc-utils.prov.w3c-prov-base)
(W3C PROV Representation Base)); the XSD is referenced directly via `resources` (role `schema`)
rather than duplicated locally.

## Examples

### A minimal CWL-style run (activity, plan-qualified and plain association, generation)
#### xml
```xml
<?xml version='1.0' encoding='UTF-8'?>
<prov:document xmlns:ex="https://example.org/cwlprov/" xmlns:prov="http://www.w3.org/ns/prov#" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <prov:entity prov:id="ex:plan/main"/>
  <prov:activity prov:id="ex:activity/step1">
    <prov:startTime>2024-01-01T00:00:00+00:00</prov:startTime>
    <prov:endTime>2024-01-01T00:01:00+00:00</prov:endTime>
  </prov:activity>
  <prov:softwareAgent prov:id="ex:engine/cwltool"/>
  <prov:wasAssociatedWith>
    <prov:activity prov:ref="ex:activity/step1"/>
    <prov:agent prov:ref="ex:engine/cwltool"/>
    <prov:plan prov:ref="ex:plan/main"/>
  </prov:wasAssociatedWith>
  <prov:wasAssociatedWith>
    <prov:activity prov:ref="ex:activity/step1"/>
    <prov:agent prov:ref="ex:engine/cwltool"/>
  </prov:wasAssociatedWith>
  <prov:entity prov:id="ex:data/output.txt"/>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="ex:data/output.txt"/>
    <prov:activity prov:ref="ex:activity/step1"/>
  </prov:wasGeneratedBy>
</prov:document>

```


### A real-world cwltool provenance run, as used in the OGC API - Processes Provenance Extension (https://docs.ogc.org/DRAFTS/26-038.html), re-serialized from the extension's job_prov.json PROV-JSON fixture with the `prov` library to guarantee it is byte-for-byte the same document as the other profiles' "ogcapi-processes-job" examples
#### xml
```xml
<?xml version='1.0' encoding='ASCII'?>
<prov:document xmlns:wfprov="http://purl.org/wf4ever/wfprov#" xmlns:wfdesc="http://purl.org/wf4ever/wfdesc#" xmlns:cwlprov="https://w3id.org/cwl/prov#" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:schema="http://schema.org/" xmlns:orcid="https://orcid.org/" xmlns:id="urn:uuid:" xmlns:data="urn:hash::sha1:" xmlns:sha256="nih:sha-256;" xmlns:researchobject="arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/" xmlns:metadata="arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/metadata/" xmlns:provenance="arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/metadata/provenance/" xmlns:wf="arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/workflow/packed.cwl#" xmlns:input="arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/workflow/primary-job.json#" xmlns:doi="https://doi.org/" xmlns:wf4ever="http://purl.org/wf4ever/wf4ever#" xmlns:loc0="https://hirondelle.crim.ca/" xmlns:loc1="https://github.com/crim-ca/" xmlns:loc2="http://pavics-weaver.readthedocs.org/en/" xmlns:loc3="https://hirondelle.crim.ca/weaver/processes/EchoProcess/jobs/" xmlns:loc4="https://hirondelle.crim.ca/weaver/processes/" xmlns:prov="http://www.w3.org/ns/prov#" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <prov:agent prov:id="id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"/>
  <prov:agent prov:id="id:dc49c9ee-a913-4e5c-b89a-2201af36af9c">
    <prov:location xsi:type="xsd:QName">loc0:weaver</prov:location>
    <prov:type xsi:type="xsd:QName">foaf:OnlineAccount</prov:type>
    <cwlprov:hostname>hirondelle.crim.ca</cwlprov:hostname>
  </prov:agent>
  <prov:agent prov:id="id:dc49c9ee-a913-4e5c-b89a-2201af36af9c">
    <prov:label>weaver-worker@crim-ca/weaver:6.9.0-dev2</prov:label>
    <prov:type xsi:type="xsd:QName">foaf:OnlineAccount</prov:type>
    <foaf:accountName>weaver-worker@crim-ca/weaver:6.9.0-dev2</foaf:accountName>
  </prov:agent>
  <prov:softwareAgent prov:id="id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990">
    <prov:label>weaver-worker@crim-ca/weaver:6.9.0-dev2</prov:label>
    <prov:type xsi:type="xsd:QName">schema:SoftwareApplication</prov:type>
    <foaf:account xsi:type="xsd:QName">id:dc49c9ee-a913-4e5c-b89a-2201af36af9c</foaf:account>
    <foaf:name>weaver-worker@crim-ca/weaver:6.9.0-dev2</foaf:name>
    <schema:name>weaver-worker@crim-ca/weaver:6.9.0-dev2</schema:name>
  </prov:softwareAgent>
  <prov:softwareAgent prov:id="id:d57aaff6-a93f-4927-a2d8-112beb358d4d">
    <prov:label>cwltool 3.1.20260108082145</prov:label>
    <prov:type xsi:type="xsd:QName">wfprov:WorkflowEngine</prov:type>
  </prov:softwareAgent>
  <prov:softwareAgent prov:id="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067">
    <prov:label>Weaver is an Execution Management Service (EMS) that allows the execution of workflows chaining various applications and Web Processing Services (WPS) inputs and outputs. Remote execution is deferred by the EMS to an Application Deployment and Execution Service (ADES), as defined by Common Workflow Language (CWL) configurations.</prov:label>
    <prov:label>crim-ca/weaver:6.9.0-dev2</prov:label>
    <prov:location xsi:type="xsd:QName">loc0:weaver</prov:location>
    <prov:generalEntity prov:ref="data:_644e201526525f62152815a76a2dc773450f3dd9"/>
    <prov:specificEntity prov:ref="doi:_10.5281_zenodo.14210717"/>
  </prov:softwareAgent>
  <prov:actedOnBehalfOf>
    <prov:delegate prov:ref="id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"/>
    <prov:responsible prov:ref="id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990"/>
  </prov:actedOnBehalfOf>
  <prov:actedOnBehalfOf>
    <prov:delegate prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"/>
    <prov:responsible prov:ref="id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990"/>
  </prov:actedOnBehalfOf>
  <prov:wasStartedBy>
    <prov:activity prov:ref="id:d57aaff6-a93f-4927-a2d8-112beb358d4d"/>
    <prov:starter prov:ref="id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"/>
    <prov:time>2026-01-15T16:46:10.775855</prov:time>
  </prov:wasStartedBy>
  <prov:wasStartedBy>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:starter prov:ref="id:d57aaff6-a93f-4927-a2d8-112beb358d4d"/>
    <prov:time>2026-01-15T16:46:10.775984</prov:time>
  </prov:wasStartedBy>
  <prov:wasStartedBy>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:trigger prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"/>
  </prov:wasStartedBy>
  <prov:wasStartedBy>
    <prov:activity prov:ref="id:d57aaff6-a93f-4927-a2d8-112beb358d4d"/>
    <prov:trigger prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:45:56.964000+00:00</prov:time>
  </prov:wasStartedBy>
  <prov:activity prov:id="id:_53f5a04e-b531-466d-81be-62c34a1431ba">
    <prov:startTime>2026-01-15T16:46:10.775907</prov:startTime>
    <prov:label>Run of workflow/packed.cwl#main</prov:label>
    <prov:type xsi:type="xsd:QName">wfprov:WorkflowRun</prov:type>
  </prov:activity>
  <prov:wasAssociatedWith>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:agent prov:ref="id:d57aaff6-a93f-4927-a2d8-112beb358d4d"/>
    <prov:plan prov:ref="wf:main"/>
  </prov:wasAssociatedWith>
  <prov:hadPrimarySource prov:id="data:_644e201526525f62152815a76a2dc773450f3dd9">
    <prov:label>Source code repository</prov:label>
    <prov:location xsi:type="xsd:QName">loc1:weaver</prov:location>
  </prov:hadPrimarySource>
  <prov:organization prov:id="data:_3102f6d7a018ebae572f457d711ed7e1e7a11bc2">
    <foaf:name>Computer Research Institute of Montr&#233;al</foaf:name>
    <schema:name>Computer Research Institute of Montr&#233;al</schema:name>
  </prov:organization>
  <prov:organization prov:id="data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0">
    <prov:label>Server Provider</prov:label>
    <prov:location xsi:type="xsd:QName">loc2:latest</prov:location>
    <foaf:name>crim-ca/weaver</foaf:name>
    <schema:name>crim-ca/weaver</schema:name>
  </prov:organization>
  <prov:entity prov:id="id:_53f5a04e-b531-466d-81be-62c34a1431ba">
    <prov:label>Job Information</prov:label>
    <prov:location xsi:type="xsd:QName">loc3:53f5a04e-b531-466d-81be-62c34a1431ba</prov:location>
    <prov:type xsi:type="xsd:QName">wfdesc:ProcessRun</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess">
    <prov:label>Process Description</prov:label>
    <prov:location xsi:type="xsd:QName">loc4:EchoProcess</prov:location>
    <prov:type xsi:type="xsd:QName">wfdesc:Process</prov:type>
  </prov:entity>
  <prov:plan prov:id="wf:main">
    <prov:label>Prospective provenance</prov:label>
    <prov:type xsi:type="xsd:QName">wfdesc:Process</prov:type>
  </prov:plan>
  <prov:entity prov:id="data:_0cf60d40470fde378076afacf5812f961208a018">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <prov:value xsi:type="xsd:string">Value2</prov:value>
  </prov:entity>
  <prov:entity prov:id="data:_0cf60d40470fde378076afacf5812f961208a018">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <prov:value xsi:type="xsd:string">Value2</prov:value>
  </prov:entity>
  <prov:entity prov:id="data:_0cf60d40470fde378076afacf5812f961208a018">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <prov:value xsi:type="xsd:string">Value2</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:cb4c5d07-5b7e-435f-882c-afe14e061f4b">
    <prov:value xsi:type="xsd:double">10.3</prov:value>
  </prov:entity>
  <prov:entity prov:id="data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <prov:value xsi:type="xsd:string">2021-03-06T07:21:00</prov:value>
  </prov:entity>
  <prov:entity prov:id="data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <prov:value xsi:type="xsd:string">2021-03-06T07:21:00</prov:value>
  </prov:entity>
  <prov:entity prov:id="data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <prov:value xsi:type="xsd:string">2021-03-06T07:21:00</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:f01a7e80-f451-4047-93c0-587666a9847a">
    <prov:value xsi:type="xsd:double">3.14159</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:a19d9289-ab50-4d85-a241-4ef9a0e36deb">
    <prov:value xsi:type="xsd:int">1</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_5e4614e1-101d-4be2-8b66-24f770b3435f">
    <prov:value xsi:type="xsd:int">2</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:a45ad975-3387-4b7c-ac1c-a268c65927d1">
    <prov:value xsi:type="xsd:int">3</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f">
    <prov:value xsi:type="xsd:int">4</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:b4c63361-5926-4b48-be43-df94727a79da">
    <prov:value xsi:type="xsd:int">5</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:a68017f5-e2f6-441c-b4ad-cf94dec801d7">
    <prov:value xsi:type="xsd:int">6</prov:value>
  </prov:entity>
  <prov:collection prov:id="id:c68b1b94-7f88-4cda-87da-f5e68beabe42">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:entity prov:id="data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:_5f78096f-fce2-49b1-aa6d-941927d15dcc">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:f0020803-854b-4bd3-a70a-f6317d3a6524">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:_6e88c002-b8f6-488e-977f-21ad51073fc6">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:collection prov:id="id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:entity prov:id="data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:d4ac4ab8-25a3-4412-82b6-07b92da98795">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:ec3fe43f2db3829507e574b5b9b1b84547d48f19">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:ec3fe43f2db3829507e574b5b9b1b84547d48f19">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:c790f3f7-ac11-4d13-9c71-4d68c73ed040">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:_795e8291ebb709a1bc71824449570f94f082a02b">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:_795e8291ebb709a1bc71824449570f94f082a02b">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:_6815d3c5-fa14-4153-befe-a5fddc285b06">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:collection prov:id="id:_88e9a099-e5d4-45f9-8402-c8082168a6f0">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:entity prov:id="data:_3f88b16b3b80316d30a93bc4035da306170884e2">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="data:_3f88b16b3b80316d30a93bc4035da306170884e2">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:fc017dcf-09ec-4cbf-81ac-741b5a61b482">
    <prov:value xsi:type="xsd:double">10.3</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_0df32fa2-e262-458f-b1df-5e749c1b19f4">
    <prov:value xsi:type="xsd:double">3.14159</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_5226c081-e3dc-4963-987b-92142bd75102">
    <prov:value xsi:type="xsd:int">1</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:f30572d8-60e4-4221-80a7-cb76e1007e9a">
    <prov:value xsi:type="xsd:int">2</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:a1aa3cbf-8435-4f94-aeb6-110922551843">
    <prov:value xsi:type="xsd:int">3</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_2a95bd87-116b-42f4-8525-428de8743778">
    <prov:value xsi:type="xsd:int">4</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:bde07acc-95a9-46f6-be09-6467fa7bd8b8">
    <prov:value xsi:type="xsd:int">5</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_6d234b31-69fb-4949-b096-924f234097a1">
    <prov:value xsi:type="xsd:int">6</prov:value>
  </prov:entity>
  <prov:collection prov:id="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:entity prov:id="id:_109d6043-7fad-428f-a563-a99a4ebd6dda">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>input</cwlprov:basename>
    <cwlprov:nameext></cwlprov:nameext>
    <cwlprov:nameroot>input</cwlprov:nameroot>
  </prov:entity>
  <prov:entity prov:id="id:_5ec5c130-692c-48d5-9cef-be41cec00d11">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>input_9i61gfqe</cwlprov:basename>
    <cwlprov:nameext></cwlprov:nameext>
    <cwlprov:nameroot>input_9i61gfqe</cwlprov:nameroot>
  </prov:entity>
  <prov:entity prov:id="id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>input_50x5752r</cwlprov:basename>
    <cwlprov:nameext></cwlprov:nameext>
    <cwlprov:nameroot>input_50x5752r</cwlprov:nameroot>
  </prov:entity>
  <prov:collection prov:id="id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:entity prov:id="id:_160a1cd9-6384-4828-b627-a02e478365fb">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>input__cdpaqkt</cwlprov:basename>
    <cwlprov:nameext></cwlprov:nameext>
    <cwlprov:nameroot>input__cdpaqkt</cwlprov:nameroot>
  </prov:entity>
  <prov:entity prov:id="id:ef9384d4-880f-4398-9e10-1bce1d54e51e">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>ew-hh.tiff</cwlprov:basename>
    <cwlprov:nameext>.tiff</cwlprov:nameext>
    <cwlprov:nameroot>ew-hh</cwlprov:nameroot>
  </prov:entity>
  <prov:entity prov:id="id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>input_9mob2l0c</cwlprov:basename>
    <cwlprov:nameext></cwlprov:nameext>
    <cwlprov:nameroot>input_9mob2l0c</cwlprov:nameroot>
  </prov:entity>
  <prov:collection prov:id="id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:entity prov:id="id:fbb085ae-d3ad-4639-a448-b01188f1ce9f">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>GetFeature.json</cwlprov:basename>
    <cwlprov:nameext>.json</cwlprov:nameext>
    <cwlprov:nameroot>GetFeature</cwlprov:nameroot>
  </prov:entity>
  <prov:entity prov:id="id:_5a1aa540-dfb8-46d5-8391-0b59b865747f">
    <prov:value xsi:type="xsd:double">10.3</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_0aebe062-805e-4853-9d80-dbc5107a8bdb">
    <prov:value xsi:type="xsd:double">3.14159</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_6a99e0ba-c671-4471-aa33-4cc523e0f428">
    <prov:value xsi:type="xsd:int">1</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_64c45605-d8a9-4a56-929d-47dcad5543f1">
    <prov:value xsi:type="xsd:int">2</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f">
    <prov:value xsi:type="xsd:int">3</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:f55d0d44-4cb4-4cd2-a336-7bac9e265583">
    <prov:value xsi:type="xsd:int">4</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:c8dbab29-6641-40d9-b5c1-626872f5337d">
    <prov:value xsi:type="xsd:int">5</prov:value>
  </prov:entity>
  <prov:entity prov:id="id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150">
    <prov:value xsi:type="xsd:int">6</prov:value>
  </prov:entity>
  <prov:collection prov:id="id:_79e5fa0b-4998-46da-bbe8-920533c7940b">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:collection prov:id="id:a326f7d5-60b5-4b9d-802f-58f2411c993e">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:collection prov:id="id:_96f693e2-3eac-4a04-8887-7285b7605f49">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:collection>
  <prov:entity prov:id="data:da39a3ee5e6b4b0d3255bfef95601890afd80709">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:a9b3da73-190e-4a3a-affb-a12396f0eac3">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>stderr.log</cwlprov:basename>
    <cwlprov:nameext>.log</cwlprov:nameext>
    <cwlprov:nameroot>stderr</cwlprov:nameroot>
  </prov:entity>
  <prov:entity prov:id="data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc">
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
  </prov:entity>
  <prov:entity prov:id="id:e66cf62a-753e-459e-b2f4-06f99396ca08">
    <prov:type xsi:type="xsd:QName">wf4ever:File</prov:type>
    <prov:type xsi:type="xsd:QName">wfprov:Artifact</prov:type>
    <cwlprov:basename>stdout.log</cwlprov:basename>
    <cwlprov:nameext>.log</cwlprov:nameext>
    <cwlprov:nameroot>stdout</cwlprov:nameroot>
  </prov:entity>
  <prov:hadPrimarySource>
    <prov:generatedEntity prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"/>
    <prov:usedEntity prov:ref="data:_644e201526525f62152815a76a2dc773450f3dd9"/>
  </prov:hadPrimarySource>
  <prov:wasDerivedFrom>
    <prov:generatedEntity prov:ref="id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"/>
    <prov:usedEntity prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"/>
  </prov:wasDerivedFrom>
  <prov:wasDerivedFrom>
    <prov:generatedEntity prov:ref="data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0"/>
    <prov:usedEntity prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"/>
  </prov:wasDerivedFrom>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"/>
    <prov:generalEntity prov:ref="id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:d57aaff6-a93f-4927-a2d8-112beb358d4d"/>
    <prov:generalEntity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_5f78096f-fce2-49b1-aa6d-941927d15dcc"/>
    <prov:generalEntity prov:ref="data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:f0020803-854b-4bd3-a70a-f6317d3a6524"/>
    <prov:generalEntity prov:ref="data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_6e88c002-b8f6-488e-977f-21ad51073fc6"/>
    <prov:generalEntity prov:ref="data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:d4ac4ab8-25a3-4412-82b6-07b92da98795"/>
    <prov:generalEntity prov:ref="data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:c790f3f7-ac11-4d13-9c71-4d68c73ed040"/>
    <prov:generalEntity prov:ref="data:ec3fe43f2db3829507e574b5b9b1b84547d48f19"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_6815d3c5-fa14-4153-befe-a5fddc285b06"/>
    <prov:generalEntity prov:ref="data:_795e8291ebb709a1bc71824449570f94f082a02b"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63"/>
    <prov:generalEntity prov:ref="data:_3f88b16b3b80316d30a93bc4035da306170884e2"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_109d6043-7fad-428f-a563-a99a4ebd6dda"/>
    <prov:generalEntity prov:ref="data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_5ec5c130-692c-48d5-9cef-be41cec00d11"/>
    <prov:generalEntity prov:ref="data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304"/>
    <prov:generalEntity prov:ref="data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_160a1cd9-6384-4828-b627-a02e478365fb"/>
    <prov:generalEntity prov:ref="data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:ef9384d4-880f-4398-9e10-1bce1d54e51e"/>
    <prov:generalEntity prov:ref="data:ec3fe43f2db3829507e574b5b9b1b84547d48f19"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9"/>
    <prov:generalEntity prov:ref="data:_795e8291ebb709a1bc71824449570f94f082a02b"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:fbb085ae-d3ad-4639-a448-b01188f1ce9f"/>
    <prov:generalEntity prov:ref="data:_3f88b16b3b80316d30a93bc4035da306170884e2"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:a9b3da73-190e-4a3a-affb-a12396f0eac3"/>
    <prov:generalEntity prov:ref="data:da39a3ee5e6b4b0d3255bfef95601890afd80709"/>
  </prov:specializationOf>
  <prov:specializationOf>
    <prov:specificEntity prov:ref="id:e66cf62a-753e-459e-b2f4-06f99396ca08"/>
    <prov:generalEntity prov:ref="data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc"/>
  </prov:specializationOf>
  <prov:wasAttributedTo>
    <prov:entity prov:ref="data:_3102f6d7a018ebae572f457d711ed7e1e7a11bc2"/>
    <prov:agent prov:ref="data:_644e201526525f62152815a76a2dc773450f3dd9"/>
  </prov:wasAttributedTo>
  <prov:wasAttributedTo>
    <prov:entity prov:ref="data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0"/>
    <prov:agent prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"/>
  </prov:wasAttributedTo>
  <prov:alternateOf>
    <prov:alternate1 prov:ref="id:d57aaff6-a93f-4927-a2d8-112beb358d4d"/>
    <prov:alternate2 prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
  </prov:alternateOf>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:activity prov:ref="data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess"/>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="data:_0cf60d40470fde378076afacf5812f961208a018"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_stringOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:_5a1aa540-dfb8-46d5-8391-0b59b865747f"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_measureOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_dateOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:_0aebe062-805e-4853-9d80-dbc5107a8bdb"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_doubleOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:_79e5fa0b-4998-46da-bbe8-920533c7940b"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_arrayOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:_109d6043-7fad-428f-a563-a99a4ebd6dda"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_complexObjectOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:a326f7d5-60b5-4b9d-802f-58f2411c993e"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_geometryOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:_160a1cd9-6384-4828-b627-a02e478365fb"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_boundingBoxOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:_96f693e2-3eac-4a04-8887-7285b7605f49"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_imagesOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:fbb085ae-d3ad-4639-a448-b01188f1ce9f"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_featureCollectionOutput</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:a9b3da73-190e-4a3a-affb-a12396f0eac3"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_a5f8bd13-1ab3-4633-9219-810292b59056</prov:role>
  </prov:wasGeneratedBy>
  <prov:wasGeneratedBy>
    <prov:entity prov:ref="id:e66cf62a-753e-459e-b2f4-06f99396ca08"/>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:time>2026-01-15T16:46:11.414795</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_b62df1f5-a3e7-412c-bdc0-0451aa8a4d93</prov:role>
  </prov:wasGeneratedBy>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="data:_0cf60d40470fde378076afacf5812f961208a018"/>
    <prov:time>2026-01-15T16:46:10.807817</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_stringInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:cb4c5d07-5b7e-435f-882c-afe14e061f4b"/>
    <prov:time>2026-01-15T16:46:10.807975</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_measureInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72"/>
    <prov:time>2026-01-15T16:46:10.808789</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_dateInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:f01a7e80-f451-4047-93c0-587666a9847a"/>
    <prov:time>2026-01-15T16:46:10.808944</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_doubleInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:c68b1b94-7f88-4cda-87da-f5e68beabe42"/>
    <prov:time>2026-01-15T16:46:10.809545</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_arrayInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_5f78096f-fce2-49b1-aa6d-941927d15dcc"/>
    <prov:time>2026-01-15T16:46:10.810650</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_complexObjectInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3"/>
    <prov:time>2026-01-15T16:46:10.812817</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_geometryInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:d4ac4ab8-25a3-4412-82b6-07b92da98795"/>
    <prov:time>2026-01-15T16:46:10.813646</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_boundingBoxInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_88e9a099-e5d4-45f9-8402-c8082168a6f0"/>
    <prov:time>2026-01-15T16:46:11.100961</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_imagesInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63"/>
    <prov:time>2026-01-15T16:46:11.101847</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_featureCollectionInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="data:_0cf60d40470fde378076afacf5812f961208a018"/>
    <prov:time>2026-01-15T16:46:11.105949</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_stringInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:fc017dcf-09ec-4cbf-81ac-741b5a61b482"/>
    <prov:time>2026-01-15T16:46:11.106052</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_measureInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72"/>
    <prov:time>2026-01-15T16:46:11.106625</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_dateInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_0df32fa2-e262-458f-b1df-5e749c1b19f4"/>
    <prov:time>2026-01-15T16:46:11.106731</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_doubleInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1"/>
    <prov:time>2026-01-15T16:46:11.107097</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_arrayInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_109d6043-7fad-428f-a563-a99a4ebd6dda"/>
    <prov:time>2026-01-15T16:46:11.107662</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_complexObjectInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823"/>
    <prov:time>2026-01-15T16:46:11.108679</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_geometryInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:_160a1cd9-6384-4828-b627-a02e478365fb"/>
    <prov:time>2026-01-15T16:46:11.109174</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_boundingBoxInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5"/>
    <prov:time>2026-01-15T16:46:11.401124</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_imagesInput</prov:role>
  </prov:used>
  <prov:used>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:entity prov:ref="id:fbb085ae-d3ad-4639-a448-b01188f1ce9f"/>
    <prov:time>2026-01-15T16:46:11.401851</prov:time>
    <prov:role xsi:type="xsd:QName">wf:main_EchoProcess_featureCollectionInput</prov:role>
  </prov:used>
  <prov:hadMember>
    <prov:collection prov:ref="id:c68b1b94-7f88-4cda-87da-f5e68beabe42"/>
    <prov:entity prov:ref="id:a19d9289-ab50-4d85-a241-4ef9a0e36deb"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:c68b1b94-7f88-4cda-87da-f5e68beabe42"/>
    <prov:entity prov:ref="id:_5e4614e1-101d-4be2-8b66-24f770b3435f"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:c68b1b94-7f88-4cda-87da-f5e68beabe42"/>
    <prov:entity prov:ref="id:a45ad975-3387-4b7c-ac1c-a268c65927d1"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:c68b1b94-7f88-4cda-87da-f5e68beabe42"/>
    <prov:entity prov:ref="id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:c68b1b94-7f88-4cda-87da-f5e68beabe42"/>
    <prov:entity prov:ref="id:b4c63361-5926-4b48-be43-df94727a79da"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:c68b1b94-7f88-4cda-87da-f5e68beabe42"/>
    <prov:entity prov:ref="id:a68017f5-e2f6-441c-b4ad-cf94dec801d7"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3"/>
    <prov:entity prov:ref="id:f0020803-854b-4bd3-a70a-f6317d3a6524"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3"/>
    <prov:entity prov:ref="id:_6e88c002-b8f6-488e-977f-21ad51073fc6"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_88e9a099-e5d4-45f9-8402-c8082168a6f0"/>
    <prov:entity prov:ref="id:c790f3f7-ac11-4d13-9c71-4d68c73ed040"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_88e9a099-e5d4-45f9-8402-c8082168a6f0"/>
    <prov:entity prov:ref="id:_6815d3c5-fa14-4153-befe-a5fddc285b06"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1"/>
    <prov:entity prov:ref="id:_5226c081-e3dc-4963-987b-92142bd75102"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1"/>
    <prov:entity prov:ref="id:f30572d8-60e4-4221-80a7-cb76e1007e9a"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1"/>
    <prov:entity prov:ref="id:a1aa3cbf-8435-4f94-aeb6-110922551843"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1"/>
    <prov:entity prov:ref="id:_2a95bd87-116b-42f4-8525-428de8743778"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1"/>
    <prov:entity prov:ref="id:bde07acc-95a9-46f6-be09-6467fa7bd8b8"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_541c0738-ac5c-4a35-b592-a3cbc87246f1"/>
    <prov:entity prov:ref="id:_6d234b31-69fb-4949-b096-924f234097a1"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823"/>
    <prov:entity prov:ref="id:_5ec5c130-692c-48d5-9cef-be41cec00d11"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823"/>
    <prov:entity prov:ref="id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5"/>
    <prov:entity prov:ref="id:ef9384d4-880f-4398-9e10-1bce1d54e51e"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5"/>
    <prov:entity prov:ref="id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_79e5fa0b-4998-46da-bbe8-920533c7940b"/>
    <prov:entity prov:ref="id:_6a99e0ba-c671-4471-aa33-4cc523e0f428"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_79e5fa0b-4998-46da-bbe8-920533c7940b"/>
    <prov:entity prov:ref="id:_64c45605-d8a9-4a56-929d-47dcad5543f1"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_79e5fa0b-4998-46da-bbe8-920533c7940b"/>
    <prov:entity prov:ref="id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_79e5fa0b-4998-46da-bbe8-920533c7940b"/>
    <prov:entity prov:ref="id:f55d0d44-4cb4-4cd2-a336-7bac9e265583"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_79e5fa0b-4998-46da-bbe8-920533c7940b"/>
    <prov:entity prov:ref="id:c8dbab29-6641-40d9-b5c1-626872f5337d"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_79e5fa0b-4998-46da-bbe8-920533c7940b"/>
    <prov:entity prov:ref="id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:a326f7d5-60b5-4b9d-802f-58f2411c993e"/>
    <prov:entity prov:ref="id:_5ec5c130-692c-48d5-9cef-be41cec00d11"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:a326f7d5-60b5-4b9d-802f-58f2411c993e"/>
    <prov:entity prov:ref="id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_96f693e2-3eac-4a04-8887-7285b7605f49"/>
    <prov:entity prov:ref="id:ef9384d4-880f-4398-9e10-1bce1d54e51e"/>
  </prov:hadMember>
  <prov:hadMember>
    <prov:collection prov:ref="id:_96f693e2-3eac-4a04-8887-7285b7605f49"/>
    <prov:entity prov:ref="id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9"/>
  </prov:hadMember>
  <prov:wasEndedBy>
    <prov:activity prov:ref="id:_53f5a04e-b531-466d-81be-62c34a1431ba"/>
    <prov:ender prov:ref="id:d57aaff6-a93f-4927-a2d8-112beb358d4d"/>
    <prov:time>2026-01-15T16:46:11.419318</prov:time>
  </prov:wasEndedBy>
</prov:document>

```

## Sources

* [PROV-XML: The PROV XML Schema](https://www.w3.org/TR/prov-xml/)
* [OGC API - Processes - Part 5: Provenance (registers `application/provenance+xml`, with `application/xml`/`text/xml` as accepted aliases, for PROV-XML)](https://docs.ogc.org/DRAFTS/26-038.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-prov-jsonld-alt](https://github.com/ogcincubator/bblocks-prov-jsonld-alt)
* Path: `_sources/prov/w3c-prov-xml`

