
# W3C PROV-JSONLD (Schema)

`ogc.ogc-utils.prov.w3c-prov-jsonld` *v0.1*

The PROV-JSONLD serialization: a non-normative, linked-data JSON-LD encoding of the W3C PROV data model (W3C Member Submission), using `@context`/`@graph` rather than the flat statement-keyed layout of PROV-JSON. A profile of the W3C PROV Representation Base.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

# W3C PROV-JSONLD

PROV-JSONLD is a non-normative W3C Member Submission JSON-LD binding of PROV-DM: a single
`@context` (this repository plus the vocabulary at the referenced `context.jsonld`) and a flat
`@graph` array of typed records — as opposed to the nested "Provenance Chain" representation from
`bblock-prov-schema`'s `ogc.ogc-utils.prov` (OGC PROV Chain) (see the
[transform](#transforms) below) or the flat but non-linked-data
`ogc.ogc-utils.prov.w3c-prov-json` (W3C PROV-JSON).

`schema` and `ldContext` reference the authoritative documents directly rather than vendoring
copies, so this block always tracks the upstream submission.

## `prov:mentionOf` / bundle mentions

The `prov` Python library's native PROV-JSONLD serializer does not support `prov:Mention` /
`prov:mentionOf` (it raises `ProvJSONLDException`) — those terms were removed from PROV-DM's final
Recommendation and now live only in the non-normative
[PROV-Links](https://www.w3.org/TR/prov-links/) note. The example below shows the accepted
workaround: `prov:specializationOf` plus a plain `prov:asInBundle` attribute, which serializes
correctly in every PROV representation, including PROV-JSONLD.

## Transforms

This block acts as the **hub** for converting between W3C PROV representations and between W3C
PROV and OGC PROV Chain: every transform either converts something *into* PROV-JSONLD or
converts PROV-JSONLD *into* something else, all implemented in Python using the `prov` library
and explicitly named for the two representations each one bridges.

**Bridging to OGC PROV Chain:**

- `w3c-prov-jsonld-to-ogc-prov-chain` - converts a **W3C PROV-JSONLD** document into the flat
  **array** form of **OGC PROV Chain** (validated against
  `ogc.ogc-utils.prov` (OGC PROV Chain)). Always emits the array form with
  full-IRI identifiers, since a generic converter can't assume a single natural root exists for
  arbitrary input.
- `ogc-prov-chain-to-w3c-prov-jsonld` - converts the flat array form of an **OGC PROV Chain**
  document back into **W3C PROV-JSONLD**.

If a single-object OGC PROV Chain result is needed instead of the array form, chain the first
transform's output into `ogc-prov-chain-array-to-object` from the
`ogc.ogc-utils.prov.ogc-prov-chain-forms` (OGC PROV Chain: Array ⇄ Object Conversion) block - that block
also provides the reverse (`ogc-prov-chain-object-to-array`) for feeding a single-object
document into `ogc-prov-chain-to-w3c-prov-jsonld`. That block's README explains why
array→object is only conditionally applicable while object→array always is.

**Bridging to/from the other W3C PROV representations:**

| Transform | Direction |
|---|---|
| `w3c-prov-json-to-w3c-prov-jsonld` | PROV-JSON → PROV-JSONLD |
| `w3c-prov-jsonld-to-w3c-prov-json` | PROV-JSONLD → PROV-JSON |
| `w3c-prov-rdf-to-w3c-prov-jsonld` | PROV-O/RDF (Turtle) → PROV-JSONLD |
| `w3c-prov-jsonld-to-w3c-prov-rdf` | PROV-JSONLD → PROV-O/RDF (Turtle) |
| `w3c-prov-xml-to-w3c-prov-jsonld` | PROV-XML → PROV-JSONLD |
| `w3c-prov-jsonld-to-w3c-prov-xml` | PROV-JSONLD → PROV-XML |
| `w3c-prov-jsonld-to-w3c-prov-n` | PROV-JSONLD → PROV-N (one-way only) |

Combining these with the OGC PROV Chain transforms above gives every W3C PROV representation a
path to and from OGC PROV Chain via PROV-JSONLD as an intermediate step - e.g. PROV-XML → PROV-JSONLD
→ OGC PROV Chain (array) → (optionally) OGC PROV Chain (object), without needing a separate
direct transform for every pair of representations.

**PROV-N is a one-way exception:** `prov` implements a PROV-N *serializer* but not a *parser*
(`ProvDocument.deserialize(..., format="provn")` raises `NotImplementedError`), so no transform
here (or anywhere in this repository) can take PROV-N as input. To convert data available only
as PROV-N into another representation, start from that data's original PROV-JSON/XML/RDF source
instead, if available.

**Note on `w3c-prov-rdf-to-w3c-prov-jsonld` and QName-unsafe identifiers:** `prov`'s RDF
deserializer requires every prefixed name (CURIE) it re-derives while reading Turtle to be
coercible to an XML `QName`/NCName local part, which must start with a letter or underscore and
cannot contain `/`, `#`, or `:`. Some real-world identifiers are not QName-safe under their
natural namespace split - e.g. `doi:10.5281/zenodo.14210717` (a slash in the local part) or
SHA1/SHA256 hash-based identifiers such as `data:644e201526525f62152815a76a2dc773450f3dd9` (a
digit-leading local part, common since hex digests often start with `0`-`9`). The
`example-ogcapi-processes-job` example's regeneration script sanitizes the local part of every
such identifier in place (e.g. `644e201526525f62152815a76a2dc773450f3dd9` ->
`_644e201526525f62152815a76a2dc773450f3dd9`), **keeping each identifier's original namespace
unchanged** rather than splitting off a new, narrower one: introducing many one-off sub-namespaces
that overlap an existing broader namespace was found to make `prov`'s namespace reconciliation
ambiguous, non-deterministically corrupting RDF re-serialization. The fix is applied to every
occurrence of the identifier (both as a record identifier and as any attribute value referencing
it), so every representation - including this transform - round-trips it correctly.

## Examples

### A minimal CWL-style run (activity, plan-qualified and plain association, generation, bundle mention via asInBundle)
#### jsonld
```jsonld
{
  "@context": [
    {
      "ex": "https://example.org/cwlprov/"
    },
    "https://openprovenance.org/prov-jsonld/context.jsonld"
  ],
  "@graph": [
    {
      "@type": "Entity",
      "@id": "ex:plan/main"
    },
    {
      "@type": "Activity",
      "@id": "ex:activity/step1",
      "startTime": "2024-01-01T00:00:00+00:00",
      "endTime": "2024-01-01T00:01:00+00:00"
    },
    {
      "@type": "Agent",
      "@id": "ex:engine/cwltool",
      "type": [
        "prov:SoftwareAgent"
      ]
    },
    {
      "@type": "Association",
      "activity": "ex:activity/step1",
      "agent": "ex:engine/cwltool",
      "plan": "ex:plan/main"
    },
    {
      "@type": "Association",
      "activity": "ex:activity/step1",
      "agent": "ex:engine/cwltool"
    },
    {
      "@type": "Entity",
      "@id": "ex:data/output.txt"
    },
    {
      "@type": "Generation",
      "entity": "ex:data/output.txt",
      "activity": "ex:activity/step1"
    },
    {
      "@type": "Specialization",
      "specificEntity": "ex:data/output.txt",
      "generalEntity": "ex:data/output.txt"
    },
    {
      "@type": "Entity",
      "@id": "ex:data/output.txt",
      "prov:asInBundle": [
        {
          "@value": "ex:bundle/nested-run",
          "@type": "xsd:QName"
        }
      ]
    },
    {
      "@type": "Bundle",
      "@id": "ex:bundle/nested-run",
      "@context": [],
      "@graph": [
        {
          "@type": "Entity",
          "@id": "ex:data/output.txt"
        }
      ]
    }
  ]
}
```

#### ttl
```ttl
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix provext: <https://openprovenance.org/ns/provext#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<ex:bundle/nested-run> a <file:///github/workspace/Bundle> .

<https://example.org/cwlprov/activity/step1> a prov:Activity ;
    prov:endedAtTime "2024-01-01T00:01:00+00:00"^^xsd:dateTime ;
    prov:qualifiedAssociation [ a prov:Association ;
            prov:agent <https://example.org/cwlprov/engine/cwltool> ],
        [ a prov:Association ;
            prov:agent <https://example.org/cwlprov/engine/cwltool> ;
            prov:hadPlan <https://example.org/cwlprov/plan/main> ] ;
    prov:startedAtTime "2024-01-01T00:00:00+00:00"^^xsd:dateTime .

<https://example.org/cwlprov/data/output.txt> a prov:Entity ;
    prov:asInBundle "ex:bundle/nested-run"^^xsd:QName ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity <https://example.org/cwlprov/activity/step1> ] ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity <https://example.org/cwlprov/data/output.txt> ] .

<https://example.org/cwlprov/plan/main> a prov:Entity .

<https://example.org/cwlprov/engine/cwltool> a prov:Agent,
        prov:SoftwareAgent .


```


### A real-world cwltool provenance run, as used in the OGC API - Processes Provenance Extension (https://docs.ogc.org/DRAFTS/26-038.html). The extension's own job_prov.jsonld fixture predates a fix and is a bare top-level array with no `@context`/`@graph` wrapper - not valid PROV-JSONLD (see https://github.com/common-workflow-language/cwltool/pull/2349, which switched cwltool to `ProvDocument.serialize(format="jsonld")` from `prov` 3.1.0's native PROV-JSONLD serializer instead of a manual RDF-graph-patching workaround). This example is re-serialized from the extension's job_prov.json PROV-JSON fixture with that same native serializer, producing the correctly-wrapped `{"@context": [...], "@graph": [...]}` shape; it is byte-for-byte the same document as the other profiles' "ogcapi-processes-job" examples
#### jsonld
```jsonld
{
  "@context": [
    {
      "wfprov": "http://purl.org/wf4ever/wfprov#",
      "wfdesc": "http://purl.org/wf4ever/wfdesc#",
      "cwlprov": "https://w3id.org/cwl/prov#",
      "foaf": "http://xmlns.com/foaf/0.1/",
      "schema": "http://schema.org/",
      "orcid": "https://orcid.org/",
      "id": "urn:uuid:",
      "data": "urn:hash::sha1:",
      "sha256": "nih:sha-256;",
      "researchobject": "arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/",
      "metadata": "arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/metadata/",
      "provenance": "arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/metadata/provenance/",
      "wf": "arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/workflow/packed.cwl#",
      "input": "arcp://uuid,53f5a04e-b531-466d-81be-62c34a1431ba/workflow/primary-job.json#",
      "doi": "https://doi.org/",
      "wf4ever": "http://purl.org/wf4ever/wf4ever#",
      "loc0": "https://hirondelle.crim.ca/",
      "loc1": "https://github.com/crim-ca/",
      "loc2": "http://pavics-weaver.readthedocs.org/en/",
      "loc3": "https://hirondelle.crim.ca/weaver/processes/EchoProcess/jobs/",
      "loc4": "https://hirondelle.crim.ca/weaver/processes/"
    },
    "https://openprovenance.org/prov-jsonld/context.jsonld"
  ],
  "@graph": [
    {
      "@type": "Agent",
      "@id": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"
    },
    {
      "@type": "Agent",
      "@id": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c",
      "type": [
        "foaf:OnlineAccount"
      ],
      "location": [
        "loc0:weaver"
      ],
      "cwlprov:hostname": [
        {
          "@value": "hirondelle.crim.ca"
        }
      ]
    },
    {
      "@type": "Agent",
      "@id": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c",
      "type": [
        "foaf:OnlineAccount"
      ],
      "label": [
        {
          "@value": "weaver-worker@crim-ca/weaver:6.9.0-dev2"
        }
      ],
      "foaf:accountName": [
        {
          "@value": "weaver-worker@crim-ca/weaver:6.9.0-dev2"
        }
      ]
    },
    {
      "@type": "Agent",
      "@id": "id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990",
      "type": [
        "prov:SoftwareAgent",
        "schema:SoftwareApplication"
      ],
      "label": [
        {
          "@value": "weaver-worker@crim-ca/weaver:6.9.0-dev2"
        }
      ],
      "foaf:name": [
        {
          "@value": "weaver-worker@crim-ca/weaver:6.9.0-dev2"
        }
      ],
      "foaf:account": [
        {
          "@value": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c",
          "@type": "xsd:QName"
        }
      ],
      "schema:name": [
        {
          "@value": "weaver-worker@crim-ca/weaver:6.9.0-dev2"
        }
      ]
    },
    {
      "@type": "Agent",
      "@id": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "type": [
        "prov:SoftwareAgent",
        "wfprov:WorkflowEngine"
      ],
      "label": [
        {
          "@value": "cwltool 3.1.20260108082145"
        }
      ]
    },
    {
      "@type": "Agent",
      "@id": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067",
      "prov:generalEntity": [
        {
          "@value": "data:_644e201526525f62152815a76a2dc773450f3dd9",
          "@type": "xsd:QName"
        }
      ],
      "prov:specificEntity": [
        {
          "@value": "doi:_10.5281_zenodo.14210717",
          "@type": "xsd:QName"
        }
      ],
      "type": [
        "prov:SoftwareAgent"
      ],
      "location": [
        "loc0:weaver"
      ],
      "label": [
        {
          "@value": "crim-ca/weaver:6.9.0-dev2"
        },
        {
          "@value": "Weaver is an Execution Management Service (EMS) that allows the execution of workflows chaining various applications and Web Processing Services (WPS) inputs and outputs. Remote execution is deferred by the EMS to an Application Deployment and Execution Service (ADES), as defined by Common Workflow Language (CWL) configurations."
        }
      ]
    },
    {
      "@type": "Delegation",
      "delegate": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c",
      "responsible": "id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990"
    },
    {
      "@type": "Delegation",
      "delegate": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067",
      "responsible": "id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990"
    },
    {
      "@type": "Start",
      "activity": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "starter": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c",
      "time": "2026-01-15T16:46:10.775855"
    },
    {
      "@type": "Start",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "starter": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "time": "2026-01-15T16:46:10.775984"
    },
    {
      "@type": "Start",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "trigger": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"
    },
    {
      "@type": "Start",
      "activity": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "trigger": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:45:56.964000+00:00"
    },
    {
      "@type": "Activity",
      "@id": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "startTime": "2026-01-15T16:46:10.775907",
      "type": [
        "wfprov:WorkflowRun"
      ],
      "label": [
        {
          "@value": "Run of workflow/packed.cwl#main"
        }
      ]
    },
    {
      "@type": "Association",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "agent": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "plan": "wf:main"
    },
    {
      "@type": "Entity",
      "@id": "data:_644e201526525f62152815a76a2dc773450f3dd9",
      "type": [
        "prov:PrimarySource"
      ],
      "label": [
        {
          "@value": "Source code repository"
        }
      ],
      "location": [
        "loc1:weaver"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_3102f6d7a018ebae572f457d711ed7e1e7a11bc2",
      "type": [
        "prov:Organization"
      ],
      "foaf:name": [
        {
          "@value": "Computer Research Institute of Montr\u00e9al"
        }
      ],
      "schema:name": [
        {
          "@value": "Computer Research Institute of Montr\u00e9al"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0",
      "foaf:name": [
        {
          "@value": "crim-ca/weaver"
        }
      ],
      "schema:name": [
        {
          "@value": "crim-ca/weaver"
        }
      ],
      "location": [
        "loc2:latest"
      ],
      "type": [
        "prov:Organization"
      ],
      "label": [
        {
          "@value": "Server Provider"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "type": [
        "wfdesc:ProcessRun"
      ],
      "location": [
        "loc3:53f5a04e-b531-466d-81be-62c34a1431ba"
      ],
      "label": [
        {
          "@value": "Job Information"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess",
      "type": [
        "wfdesc:Process"
      ],
      "location": [
        "loc4:EchoProcess"
      ],
      "label": [
        {
          "@value": "Process Description"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "wf:main",
      "type": [
        "wfdesc:Process",
        "prov:Plan"
      ],
      "label": [
        {
          "@value": "Prospective provenance"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_0cf60d40470fde378076afacf5812f961208a018",
      "type": [
        "wfprov:Artifact"
      ],
      "value": [
        {
          "@value": "Value2"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_0cf60d40470fde378076afacf5812f961208a018",
      "type": [
        "wfprov:Artifact"
      ],
      "value": [
        {
          "@value": "Value2"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_0cf60d40470fde378076afacf5812f961208a018",
      "type": [
        "wfprov:Artifact"
      ],
      "value": [
        {
          "@value": "Value2"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:cb4c5d07-5b7e-435f-882c-afe14e061f4b",
      "value": [
        {
          "@value": "10.3",
          "@type": "xsd:double"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72",
      "type": [
        "wfprov:Artifact"
      ],
      "value": [
        {
          "@value": "2021-03-06T07:21:00"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72",
      "type": [
        "wfprov:Artifact"
      ],
      "value": [
        {
          "@value": "2021-03-06T07:21:00"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72",
      "type": [
        "wfprov:Artifact"
      ],
      "value": [
        {
          "@value": "2021-03-06T07:21:00"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:f01a7e80-f451-4047-93c0-587666a9847a",
      "value": [
        {
          "@value": "3.14159",
          "@type": "xsd:double"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:a19d9289-ab50-4d85-a241-4ef9a0e36deb",
      "value": [
        {
          "@value": "1",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_5e4614e1-101d-4be2-8b66-24f770b3435f",
      "value": [
        {
          "@value": "2",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:a45ad975-3387-4b7c-ac1c-a268c65927d1",
      "value": [
        {
          "@value": "3",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f",
      "value": [
        {
          "@value": "4",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:b4c63361-5926-4b48-be43-df94727a79da",
      "value": [
        {
          "@value": "5",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:a68017f5-e2f6-441c-b4ad-cf94dec801d7",
      "value": [
        {
          "@value": "6",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_5f78096f-fce2-49b1-aa6d-941927d15dcc",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:f0020803-854b-4bd3-a70a-f6317d3a6524",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_6e88c002-b8f6-488e-977f-21ad51073fc6",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:d4ac4ab8-25a3-4412-82b6-07b92da98795",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:ec3fe43f2db3829507e574b5b9b1b84547d48f19",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:ec3fe43f2db3829507e574b5b9b1b84547d48f19",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:c790f3f7-ac11-4d13-9c71-4d68c73ed040",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_795e8291ebb709a1bc71824449570f94f082a02b",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_795e8291ebb709a1bc71824449570f94f082a02b",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_6815d3c5-fa14-4153-befe-a5fddc285b06",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_88e9a099-e5d4-45f9-8402-c8082168a6f0",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_3f88b16b3b80316d30a93bc4035da306170884e2",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:_3f88b16b3b80316d30a93bc4035da306170884e2",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:fc017dcf-09ec-4cbf-81ac-741b5a61b482",
      "value": [
        {
          "@value": "10.3",
          "@type": "xsd:double"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_0df32fa2-e262-458f-b1df-5e749c1b19f4",
      "value": [
        {
          "@value": "3.14159",
          "@type": "xsd:double"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_5226c081-e3dc-4963-987b-92142bd75102",
      "value": [
        {
          "@value": "1",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:f30572d8-60e4-4221-80a7-cb76e1007e9a",
      "value": [
        {
          "@value": "2",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:a1aa3cbf-8435-4f94-aeb6-110922551843",
      "value": [
        {
          "@value": "3",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_2a95bd87-116b-42f4-8525-428de8743778",
      "value": [
        {
          "@value": "4",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:bde07acc-95a9-46f6-be09-6467fa7bd8b8",
      "value": [
        {
          "@value": "5",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_6d234b31-69fb-4949-b096-924f234097a1",
      "value": [
        {
          "@value": "6",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_109d6043-7fad-428f-a563-a99a4ebd6dda",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "input"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "input"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ""
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_5ec5c130-692c-48d5-9cef-be41cec00d11",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "input_9i61gfqe"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "input_9i61gfqe"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ""
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "input_50x5752r"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "input_50x5752r"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ""
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_160a1cd9-6384-4828-b627-a02e478365fb",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "input__cdpaqkt"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "input__cdpaqkt"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ""
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:ef9384d4-880f-4398-9e10-1bce1d54e51e",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "ew-hh.tiff"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "ew-hh"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ".tiff"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "input_9mob2l0c"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "input_9mob2l0c"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ""
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:fbb085ae-d3ad-4639-a448-b01188f1ce9f",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "GetFeature.json"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "GetFeature"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ".json"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_5a1aa540-dfb8-46d5-8391-0b59b865747f",
      "value": [
        {
          "@value": "10.3",
          "@type": "xsd:double"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_0aebe062-805e-4853-9d80-dbc5107a8bdb",
      "value": [
        {
          "@value": "3.14159",
          "@type": "xsd:double"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_6a99e0ba-c671-4471-aa33-4cc523e0f428",
      "value": [
        {
          "@value": "1",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_64c45605-d8a9-4a56-929d-47dcad5543f1",
      "value": [
        {
          "@value": "2",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f",
      "value": [
        {
          "@value": "3",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:f55d0d44-4cb4-4cd2-a336-7bac9e265583",
      "value": [
        {
          "@value": "4",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:c8dbab29-6641-40d9-b5c1-626872f5337d",
      "value": [
        {
          "@value": "5",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150",
      "value": [
        {
          "@value": "6",
          "@type": "xsd:int"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:a326f7d5-60b5-4b9d-802f-58f2411c993e",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:_96f693e2-3eac-4a04-8887-7285b7605f49",
      "type": [
        "wfprov:Artifact",
        "prov:Collection"
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:da39a3ee5e6b4b0d3255bfef95601890afd80709",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:a9b3da73-190e-4a3a-affb-a12396f0eac3",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "stderr.log"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "stderr"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ".log"
        }
      ]
    },
    {
      "@type": "Entity",
      "@id": "data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc",
      "type": [
        "wfprov:Artifact"
      ]
    },
    {
      "@type": "Entity",
      "@id": "id:e66cf62a-753e-459e-b2f4-06f99396ca08",
      "type": [
        "wfprov:Artifact",
        "wf4ever:File"
      ],
      "cwlprov:basename": [
        {
          "@value": "stdout.log"
        }
      ],
      "cwlprov:nameroot": [
        {
          "@value": "stdout"
        }
      ],
      "cwlprov:nameext": [
        {
          "@value": ".log"
        }
      ]
    },
    {
      "@type": "Derivation",
      "generatedEntity": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067",
      "usedEntity": "data:_644e201526525f62152815a76a2dc773450f3dd9",
      "type": [
        "prov:PrimarySource"
      ]
    },
    {
      "@type": "Derivation",
      "generatedEntity": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c",
      "usedEntity": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"
    },
    {
      "@type": "Derivation",
      "generatedEntity": "data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0",
      "usedEntity": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"
    },
    {
      "@type": "Specialization",
      "specificEntity": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067",
      "generalEntity": "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "generalEntity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_5f78096f-fce2-49b1-aa6d-941927d15dcc",
      "generalEntity": "data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:f0020803-854b-4bd3-a70a-f6317d3a6524",
      "generalEntity": "data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_6e88c002-b8f6-488e-977f-21ad51073fc6",
      "generalEntity": "data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:d4ac4ab8-25a3-4412-82b6-07b92da98795",
      "generalEntity": "data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:c790f3f7-ac11-4d13-9c71-4d68c73ed040",
      "generalEntity": "data:ec3fe43f2db3829507e574b5b9b1b84547d48f19"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_6815d3c5-fa14-4153-befe-a5fddc285b06",
      "generalEntity": "data:_795e8291ebb709a1bc71824449570f94f082a02b"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63",
      "generalEntity": "data:_3f88b16b3b80316d30a93bc4035da306170884e2"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_109d6043-7fad-428f-a563-a99a4ebd6dda",
      "generalEntity": "data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_5ec5c130-692c-48d5-9cef-be41cec00d11",
      "generalEntity": "data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304",
      "generalEntity": "data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_160a1cd9-6384-4828-b627-a02e478365fb",
      "generalEntity": "data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:ef9384d4-880f-4398-9e10-1bce1d54e51e",
      "generalEntity": "data:ec3fe43f2db3829507e574b5b9b1b84547d48f19"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9",
      "generalEntity": "data:_795e8291ebb709a1bc71824449570f94f082a02b"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:fbb085ae-d3ad-4639-a448-b01188f1ce9f",
      "generalEntity": "data:_3f88b16b3b80316d30a93bc4035da306170884e2"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:a9b3da73-190e-4a3a-affb-a12396f0eac3",
      "generalEntity": "data:da39a3ee5e6b4b0d3255bfef95601890afd80709"
    },
    {
      "@type": "Specialization",
      "specificEntity": "id:e66cf62a-753e-459e-b2f4-06f99396ca08",
      "generalEntity": "data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc"
    },
    {
      "@type": "Attribution",
      "entity": "data:_3102f6d7a018ebae572f457d711ed7e1e7a11bc2",
      "agent": "data:_644e201526525f62152815a76a2dc773450f3dd9"
    },
    {
      "@type": "Attribution",
      "entity": "data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0",
      "agent": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067"
    },
    {
      "@type": "Alternate",
      "alternate1": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "alternate2": "id:_53f5a04e-b531-466d-81be-62c34a1431ba"
    },
    {
      "@type": "Generation",
      "entity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "activity": "data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess"
    },
    {
      "@type": "Generation",
      "entity": "data:_0cf60d40470fde378076afacf5812f961208a018",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_stringOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:_5a1aa540-dfb8-46d5-8391-0b59b865747f",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_measureOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_dateOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:_0aebe062-805e-4853-9d80-dbc5107a8bdb",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_doubleOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_arrayOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:_109d6043-7fad-428f-a563-a99a4ebd6dda",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_complexObjectOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:a326f7d5-60b5-4b9d-802f-58f2411c993e",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_geometryOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:_160a1cd9-6384-4828-b627-a02e478365fb",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_boundingBoxOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:_96f693e2-3eac-4a04-8887-7285b7605f49",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_imagesOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:fbb085ae-d3ad-4639-a448-b01188f1ce9f",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_featureCollectionOutput"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:a9b3da73-190e-4a3a-affb-a12396f0eac3",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_a5f8bd13-1ab3-4633-9219-810292b59056"
      ]
    },
    {
      "@type": "Generation",
      "entity": "id:e66cf62a-753e-459e-b2f4-06f99396ca08",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "time": "2026-01-15T16:46:11.414795",
      "role": [
        "wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_b62df1f5-a3e7-412c-bdc0-0451aa8a4d93"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "data:_0cf60d40470fde378076afacf5812f961208a018",
      "time": "2026-01-15T16:46:10.807817",
      "role": [
        "wf:main_stringInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:cb4c5d07-5b7e-435f-882c-afe14e061f4b",
      "time": "2026-01-15T16:46:10.807975",
      "role": [
        "wf:main_measureInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72",
      "time": "2026-01-15T16:46:10.808789",
      "role": [
        "wf:main_dateInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:f01a7e80-f451-4047-93c0-587666a9847a",
      "time": "2026-01-15T16:46:10.808944",
      "role": [
        "wf:main_doubleInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "time": "2026-01-15T16:46:10.809545",
      "role": [
        "wf:main_arrayInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_5f78096f-fce2-49b1-aa6d-941927d15dcc",
      "time": "2026-01-15T16:46:10.810650",
      "role": [
        "wf:main_complexObjectInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3",
      "time": "2026-01-15T16:46:10.812817",
      "role": [
        "wf:main_geometryInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:d4ac4ab8-25a3-4412-82b6-07b92da98795",
      "time": "2026-01-15T16:46:10.813646",
      "role": [
        "wf:main_boundingBoxInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_88e9a099-e5d4-45f9-8402-c8082168a6f0",
      "time": "2026-01-15T16:46:11.100961",
      "role": [
        "wf:main_imagesInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63",
      "time": "2026-01-15T16:46:11.101847",
      "role": [
        "wf:main_featureCollectionInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "data:_0cf60d40470fde378076afacf5812f961208a018",
      "time": "2026-01-15T16:46:11.105949",
      "role": [
        "wf:main_EchoProcess_stringInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:fc017dcf-09ec-4cbf-81ac-741b5a61b482",
      "time": "2026-01-15T16:46:11.106052",
      "role": [
        "wf:main_EchoProcess_measureInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72",
      "time": "2026-01-15T16:46:11.106625",
      "role": [
        "wf:main_EchoProcess_dateInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_0df32fa2-e262-458f-b1df-5e749c1b19f4",
      "time": "2026-01-15T16:46:11.106731",
      "role": [
        "wf:main_EchoProcess_doubleInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "time": "2026-01-15T16:46:11.107097",
      "role": [
        "wf:main_EchoProcess_arrayInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_109d6043-7fad-428f-a563-a99a4ebd6dda",
      "time": "2026-01-15T16:46:11.107662",
      "role": [
        "wf:main_EchoProcess_complexObjectInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823",
      "time": "2026-01-15T16:46:11.108679",
      "role": [
        "wf:main_EchoProcess_geometryInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:_160a1cd9-6384-4828-b627-a02e478365fb",
      "time": "2026-01-15T16:46:11.109174",
      "role": [
        "wf:main_EchoProcess_boundingBoxInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5",
      "time": "2026-01-15T16:46:11.401124",
      "role": [
        "wf:main_EchoProcess_imagesInput"
      ]
    },
    {
      "@type": "Usage",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "entity": "id:fbb085ae-d3ad-4639-a448-b01188f1ce9f",
      "time": "2026-01-15T16:46:11.401851",
      "role": [
        "wf:main_EchoProcess_featureCollectionInput"
      ]
    },
    {
      "@type": "Membership",
      "collection": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "entity": "id:a19d9289-ab50-4d85-a241-4ef9a0e36deb"
    },
    {
      "@type": "Membership",
      "collection": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "entity": "id:_5e4614e1-101d-4be2-8b66-24f770b3435f"
    },
    {
      "@type": "Membership",
      "collection": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "entity": "id:a45ad975-3387-4b7c-ac1c-a268c65927d1"
    },
    {
      "@type": "Membership",
      "collection": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "entity": "id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f"
    },
    {
      "@type": "Membership",
      "collection": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "entity": "id:b4c63361-5926-4b48-be43-df94727a79da"
    },
    {
      "@type": "Membership",
      "collection": "id:c68b1b94-7f88-4cda-87da-f5e68beabe42",
      "entity": "id:a68017f5-e2f6-441c-b4ad-cf94dec801d7"
    },
    {
      "@type": "Membership",
      "collection": "id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3",
      "entity": "id:f0020803-854b-4bd3-a70a-f6317d3a6524"
    },
    {
      "@type": "Membership",
      "collection": "id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3",
      "entity": "id:_6e88c002-b8f6-488e-977f-21ad51073fc6"
    },
    {
      "@type": "Membership",
      "collection": "id:_88e9a099-e5d4-45f9-8402-c8082168a6f0",
      "entity": "id:c790f3f7-ac11-4d13-9c71-4d68c73ed040"
    },
    {
      "@type": "Membership",
      "collection": "id:_88e9a099-e5d4-45f9-8402-c8082168a6f0",
      "entity": "id:_6815d3c5-fa14-4153-befe-a5fddc285b06"
    },
    {
      "@type": "Membership",
      "collection": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "entity": "id:_5226c081-e3dc-4963-987b-92142bd75102"
    },
    {
      "@type": "Membership",
      "collection": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "entity": "id:f30572d8-60e4-4221-80a7-cb76e1007e9a"
    },
    {
      "@type": "Membership",
      "collection": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "entity": "id:a1aa3cbf-8435-4f94-aeb6-110922551843"
    },
    {
      "@type": "Membership",
      "collection": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "entity": "id:_2a95bd87-116b-42f4-8525-428de8743778"
    },
    {
      "@type": "Membership",
      "collection": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "entity": "id:bde07acc-95a9-46f6-be09-6467fa7bd8b8"
    },
    {
      "@type": "Membership",
      "collection": "id:_541c0738-ac5c-4a35-b592-a3cbc87246f1",
      "entity": "id:_6d234b31-69fb-4949-b096-924f234097a1"
    },
    {
      "@type": "Membership",
      "collection": "id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823",
      "entity": "id:_5ec5c130-692c-48d5-9cef-be41cec00d11"
    },
    {
      "@type": "Membership",
      "collection": "id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823",
      "entity": "id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304"
    },
    {
      "@type": "Membership",
      "collection": "id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5",
      "entity": "id:ef9384d4-880f-4398-9e10-1bce1d54e51e"
    },
    {
      "@type": "Membership",
      "collection": "id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5",
      "entity": "id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9"
    },
    {
      "@type": "Membership",
      "collection": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "entity": "id:_6a99e0ba-c671-4471-aa33-4cc523e0f428"
    },
    {
      "@type": "Membership",
      "collection": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "entity": "id:_64c45605-d8a9-4a56-929d-47dcad5543f1"
    },
    {
      "@type": "Membership",
      "collection": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "entity": "id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f"
    },
    {
      "@type": "Membership",
      "collection": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "entity": "id:f55d0d44-4cb4-4cd2-a336-7bac9e265583"
    },
    {
      "@type": "Membership",
      "collection": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "entity": "id:c8dbab29-6641-40d9-b5c1-626872f5337d"
    },
    {
      "@type": "Membership",
      "collection": "id:_79e5fa0b-4998-46da-bbe8-920533c7940b",
      "entity": "id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150"
    },
    {
      "@type": "Membership",
      "collection": "id:a326f7d5-60b5-4b9d-802f-58f2411c993e",
      "entity": "id:_5ec5c130-692c-48d5-9cef-be41cec00d11"
    },
    {
      "@type": "Membership",
      "collection": "id:a326f7d5-60b5-4b9d-802f-58f2411c993e",
      "entity": "id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304"
    },
    {
      "@type": "Membership",
      "collection": "id:_96f693e2-3eac-4a04-8887-7285b7605f49",
      "entity": "id:ef9384d4-880f-4398-9e10-1bce1d54e51e"
    },
    {
      "@type": "Membership",
      "collection": "id:_96f693e2-3eac-4a04-8887-7285b7605f49",
      "entity": "id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9"
    },
    {
      "@type": "End",
      "activity": "id:_53f5a04e-b531-466d-81be-62c34a1431ba",
      "ender": "id:d57aaff6-a93f-4927-a2d8-112beb358d4d",
      "time": "2026-01-15T16:46:11.419318"
    }
  ]
}
```

#### ttl
```ttl
@prefix cwlprov: <https://w3id.org/cwl/prov#> .
@prefix data: <urn:hash::sha1:> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix id: <urn:uuid:> .
@prefix loc0: <https://hirondelle.crim.ca/> .
@prefix loc1: <https://github.com/crim-ca/> .
@prefix loc2: <http://pavics-weaver.readthedocs.org/en/> .
@prefix loc3: <https://hirondelle.crim.ca/weaver/processes/EchoProcess/jobs/> .
@prefix loc4: <https://hirondelle.crim.ca/weaver/processes/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix provext: <https://openprovenance.org/ns/provext#> .
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
    prov:qualifiedAttribution [ a prov:Attribution ;
            prov:agent data:_644e201526525f62152815a76a2dc773450f3dd9 ] ;
    foaf:name "Computer Research Institute of Montréal" .

data:_838cdfa4bbf09d1aedd26d79b46bfa8778ede2e0 a prov:Entity,
        prov:Organization ;
    rdfs:label "Server Provider" ;
    schema1:name "crim-ca/weaver" ;
    prov:atLocation loc2:latest ;
    prov:qualifiedAttribution [ a prov:Attribution ;
            prov:agent data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 ] ;
    prov:qualifiedDerivation [ a prov:Derivation ;
            prov:entity data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 ] ;
    foaf:name "crim-ca/weaver" .

id:_0aebe062-805e-4853-9d80-dbc5107a8bdb a prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_doubleOutput ] ;
    prov:value 3.14159e+00 .

id:_5a1aa540-dfb8-46d5-8391-0b59b865747f a prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_measureOutput ] ;
    prov:value 1.03e+01 .

id:_79e5fa0b-4998-46da-bbe8-920533c7940b a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_arrayOutput ] ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:_9718f0ee-b250-4d33-a6df-4b8ad72bf150 ],
        [ a provext:Membership ;
            provext:member id:_64c45605-d8a9-4a56-929d-47dcad5543f1 ],
        [ a provext:Membership ;
            provext:member id:b557ccae-b5e3-43ce-bc06-f39d3e12f67f ],
        [ a provext:Membership ;
            provext:member id:f55d0d44-4cb4-4cd2-a336-7bac9e265583 ],
        [ a provext:Membership ;
            provext:member id:c8dbab29-6641-40d9-b5c1-626872f5337d ],
        [ a provext:Membership ;
            provext:member id:_6a99e0ba-c671-4471-aa33-4cc523e0f428 ] .

id:_96f693e2-3eac-4a04-8887-7285b7605f49 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_imagesOutput ] ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9 ],
        [ a provext:Membership ;
            provext:member id:ef9384d4-880f-4398-9e10-1bce1d54e51e ] .

id:a326f7d5-60b5-4b9d-802f-58f2411c993e a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_geometryOutput ] ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:_5ec5c130-692c-48d5-9cef-be41cec00d11 ],
        [ a provext:Membership ;
            provext:member id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304 ] .

id:a9b3da73-190e-4a3a-affb-a12396f0eac3 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_PACKAGE_OUTPUT_HOOK_LOG_a5f8bd13-1ab3-4633-9219-810292b59056 ] ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:da39a3ee5e6b4b0d3255bfef95601890afd80709 ] ;
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
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc ] ;
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
    prov:value 3.14159e+00 .

id:_109d6043-7fad-428f-a563-a99a4ebd6dda a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity id:_53f5a04e-b531-466d-81be-62c34a1431ba ;
            prov:atTime "2026-01-15T16:46:11.414795"^^xsd:dateTime ;
            prov:hadRole wf:main_primary_complexObjectOutput ] ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c ] ;
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
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d ] ;
    cwlprov:basename "input__cdpaqkt" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input__cdpaqkt" .

id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304 ],
        [ a provext:Membership ;
            provext:member id:_5ec5c130-692c-48d5-9cef-be41cec00d11 ] .

id:_2a95bd87-116b-42f4-8525-428de8743778 a prov:Entity ;
    prov:value "4"^^xsd:int .

id:_5226c081-e3dc-4963-987b-92142bd75102 a prov:Entity ;
    prov:value "1"^^xsd:int .

id:_541c0738-ac5c-4a35-b592-a3cbc87246f1 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:bde07acc-95a9-46f6-be09-6467fa7bd8b8 ],
        [ a provext:Membership ;
            provext:member id:a1aa3cbf-8435-4f94-aeb6-110922551843 ],
        [ a provext:Membership ;
            provext:member id:_5226c081-e3dc-4963-987b-92142bd75102 ],
        [ a provext:Membership ;
            provext:member id:_2a95bd87-116b-42f4-8525-428de8743778 ],
        [ a provext:Membership ;
            provext:member id:f30572d8-60e4-4221-80a7-cb76e1007e9a ],
        [ a provext:Membership ;
            provext:member id:_6d234b31-69fb-4949-b096-924f234097a1 ] .

id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_3f88b16b3b80316d30a93bc4035da306170884e2 ] .

id:_5e4614e1-101d-4be2-8b66-24f770b3435f a prov:Entity ;
    prov:value "2"^^xsd:int .

id:_5f78096f-fce2-49b1-aa6d-941927d15dcc a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_1ed7ac15d56fc9b6257234caebf4bed6e559b53c ] .

id:_64c45605-d8a9-4a56-929d-47dcad5543f1 a prov:Entity ;
    prov:value "2"^^xsd:int .

id:_6815d3c5-fa14-4153-befe-a5fddc285b06 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_795e8291ebb709a1bc71824449570f94f082a02b ] .

id:_6a99e0ba-c671-4471-aa33-4cc523e0f428 a prov:Entity ;
    prov:value "1"^^xsd:int .

id:_6d234b31-69fb-4949-b096-924f234097a1 a prov:Entity ;
    prov:value "6"^^xsd:int .

id:_6e88c002-b8f6-488e-977f-21ad51073fc6 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5 ] .

id:_88e9a099-e5d4-45f9-8402-c8082168a6f0 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:c790f3f7-ac11-4d13-9c71-4d68c73ed040 ],
        [ a provext:Membership ;
            provext:member id:_6815d3c5-fa14-4153-befe-a5fddc285b06 ] .

id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:_6e88c002-b8f6-488e-977f-21ad51073fc6 ],
        [ a provext:Membership ;
            provext:member id:f0020803-854b-4bd3-a70a-f6317d3a6524 ] .

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
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:_043749d9-938e-4aa4-b5ae-12fc699dbcc9 ],
        [ a provext:Membership ;
            provext:member id:ef9384d4-880f-4398-9e10-1bce1d54e51e ] .

id:c68b1b94-7f88-4cda-87da-f5e68beabe42 a wfprov:Artifact,
        prov:Collection,
        prov:Entity ;
    provext:qualifiedMembership [ a provext:Membership ;
            provext:member id:a68017f5-e2f6-441c-b4ad-cf94dec801d7 ],
        [ a provext:Membership ;
            provext:member id:a19d9289-ab50-4d85-a241-4ef9a0e36deb ],
        [ a provext:Membership ;
            provext:member id:_5e4614e1-101d-4be2-8b66-24f770b3435f ],
        [ a provext:Membership ;
            provext:member id:a45ad975-3387-4b7c-ac1c-a268c65927d1 ],
        [ a provext:Membership ;
            provext:member id:_056f6ec9-f5ca-4630-8b6e-171ea0fe8f3f ],
        [ a provext:Membership ;
            provext:member id:b4c63361-5926-4b48-be43-df94727a79da ] .

id:c790f3f7-ac11-4d13-9c71-4d68c73ed040 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:ec3fe43f2db3829507e574b5b9b1b84547d48f19 ] .

id:c8dbab29-6641-40d9-b5c1-626872f5337d a prov:Entity ;
    prov:value "5"^^xsd:int .

id:cb4c5d07-5b7e-435f-882c-afe14e061f4b a prov:Entity ;
    prov:value 1.03e+01 .

id:d4ac4ab8-25a3-4412-82b6-07b92da98795 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:fc6f6f7466a49edf8dd6d0aa6d30457c85263b2d ] .

id:f0020803-854b-4bd3-a70a-f6317d3a6524 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb ] .

id:f01a7e80-f451-4047-93c0-587666a9847a a prov:Entity ;
    prov:value 3.14159e+00 .

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
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_3f88b16b3b80316d30a93bc4035da306170884e2 ] ;
    cwlprov:basename "GetFeature.json" ;
    cwlprov:nameext ".json" ;
    cwlprov:nameroot "GetFeature" .

id:fc017dcf-09ec-4cbf-81ac-741b5a61b482 a prov:Entity ;
    prov:value 1.03e+01 .

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

data:_644e201526525f62152815a76a2dc773450f3dd9 a prov:Entity,
        prov:PrimarySource ;
    rdfs:label "Source code repository" ;
    prov:atLocation loc1:weaver .

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
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_795e8291ebb709a1bc71824449570f94f082a02b ] ;
    cwlprov:basename "input_9mob2l0c" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input_9mob2l0c" .

id:_5ec5c130-692c-48d5-9cef-be41cec00d11 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:fb3b7d0ef0d175962d9a89b97cc16921cf2983eb ] ;
    cwlprov:basename "input_9i61gfqe" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input_9i61gfqe" .

id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990 a schema1:SoftwareApplication,
        prov:Agent,
        prov:SoftwareAgent ;
    rdfs:label "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    schema1:name "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    foaf:account "id:dc49c9ee-a913-4e5c-b89a-2201af36af9c"^^xsd:QName ;
    foaf:name "weaver-worker@crim-ca/weaver:6.9.0-dev2" .

id:_9c60ce13-37d4-4dd2-98f5-d1c3bea1f304 a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:_82f6bd8f98adc472eb9e350df9d64c102da0bcb5 ] ;
    cwlprov:basename "input_50x5752r" ;
    cwlprov:nameext "" ;
    cwlprov:nameroot "input_50x5752r" .

id:dc49c9ee-a913-4e5c-b89a-2201af36af9c a prov:Agent,
        foaf:OnlineAccount ;
    rdfs:label "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    prov:atLocation loc0:weaver ;
    prov:qualifiedDelegation [ a prov:Delegation ;
            prov:agent id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990 ] ;
    prov:qualifiedDerivation [ a prov:Derivation ;
            prov:entity data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 ] ;
    foaf:accountName "weaver-worker@crim-ca/weaver:6.9.0-dev2" ;
    cwlprov:hostname "hirondelle.crim.ca" .

id:ef9384d4-880f-4398-9e10-1bce1d54e51e a wf4ever:File,
        wfprov:Artifact,
        prov:Entity ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity data:ec3fe43f2db3829507e574b5b9b1b84547d48f19 ] ;
    cwlprov:basename "ew-hh.tiff" ;
    cwlprov:nameext ".tiff" ;
    cwlprov:nameroot "ew-hh" .

id:d57aaff6-a93f-4927-a2d8-112beb358d4d a wfprov:WorkflowEngine,
        prov:Agent,
        prov:SoftwareAgent ;
    rdfs:label "cwltool 3.1.20260108082145" ;
    prov:qualifiedStart [ a prov:Start ;
            prov:atTime "2026-01-15T16:46:10.775855"^^xsd:dateTime ;
            prov:hadActivity id:dc49c9ee-a913-4e5c-b89a-2201af36af9c ],
        [ a prov:Start ;
            prov:atTime "2026-01-15T16:45:56.964000+00:00"^^xsd:dateTime ;
            prov:entity id:_53f5a04e-b531-466d-81be-62c34a1431ba ] ;
    provext:qualifiedAlternate [ a provext:Alternate ;
            provext:alternate id:_53f5a04e-b531-466d-81be-62c34a1431ba ] ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity id:_53f5a04e-b531-466d-81be-62c34a1431ba ] .

data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 a prov:Agent,
        prov:SoftwareAgent ;
    rdfs:label "Weaver is an Execution Management Service (EMS) that allows the execution of workflows chaining various applications and Web Processing Services (WPS) inputs and outputs. Remote execution is deferred by the EMS to an Application Deployment and Execution Service (ADES), as defined by Common Workflow Language (CWL) configurations.",
        "crim-ca/weaver:6.9.0-dev2" ;
    prov:atLocation loc0:weaver ;
    prov:generalEntity "data:_644e201526525f62152815a76a2dc773450f3dd9"^^xsd:QName ;
    prov:qualifiedDelegation [ a prov:Delegation ;
            prov:agent id:_6e5f8b71-eb5c-45d8-a497-7f6df55e1990 ] ;
    prov:qualifiedDerivation [ a prov:Derivation,
                prov:PrimarySource ;
            prov:entity data:_644e201526525f62152815a76a2dc773450f3dd9 ] ;
    prov:specificEntity "doi:_10.5281_zenodo.14210717"^^xsd:QName ;
    provext:qualifiedSpecialization [ a provext:Specialization ;
            provext:generalEntity id:dc49c9ee-a913-4e5c-b89a-2201af36af9c ] .

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
    prov:qualifiedGeneration [ a prov:Generation ;
            prov:activity data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067_EchoProcess ] ;
    prov:qualifiedStart [ a prov:Start ;
            prov:entity data:_4e5feeeb8209de47c8dfb7c3f50a893e505af067 ],
        [ a prov:Start ;
            prov:atTime "2026-01-15T16:46:10.775984"^^xsd:dateTime ;
            prov:hadActivity id:d57aaff6-a93f-4927-a2d8-112beb358d4d ] ;
    prov:qualifiedUsage [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.808789"^^xsd:dateTime ;
            prov:entity data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72 ;
            prov:hadRole wf:main_dateInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.106625"^^xsd:dateTime ;
            prov:entity data:_9ddf13e345a6b6376bc2fa817bd4b749f4cfae72 ;
            prov:hadRole wf:main_EchoProcess_dateInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.105949"^^xsd:dateTime ;
            prov:entity data:_0cf60d40470fde378076afacf5812f961208a018 ;
            prov:hadRole wf:main_EchoProcess_stringInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.107662"^^xsd:dateTime ;
            prov:entity id:_109d6043-7fad-428f-a563-a99a4ebd6dda ;
            prov:hadRole wf:main_EchoProcess_complexObjectInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.101847"^^xsd:dateTime ;
            prov:entity id:_54f9b9d5-641c-4e66-8c9d-c65f2ad0be63 ;
            prov:hadRole wf:main_featureCollectionInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.109174"^^xsd:dateTime ;
            prov:entity id:_160a1cd9-6384-4828-b627-a02e478365fb ;
            prov:hadRole wf:main_EchoProcess_boundingBoxInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.401124"^^xsd:dateTime ;
            prov:entity id:c14eb1fb-b860-4cfb-ba2c-c9f2f4f5d4e5 ;
            prov:hadRole wf:main_EchoProcess_imagesInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.107097"^^xsd:dateTime ;
            prov:entity id:_541c0738-ac5c-4a35-b592-a3cbc87246f1 ;
            prov:hadRole wf:main_EchoProcess_arrayInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.808944"^^xsd:dateTime ;
            prov:entity id:f01a7e80-f451-4047-93c0-587666a9847a ;
            prov:hadRole wf:main_doubleInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.106731"^^xsd:dateTime ;
            prov:entity id:_0df32fa2-e262-458f-b1df-5e749c1b19f4 ;
            prov:hadRole wf:main_EchoProcess_doubleInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.100961"^^xsd:dateTime ;
            prov:entity id:_88e9a099-e5d4-45f9-8402-c8082168a6f0 ;
            prov:hadRole wf:main_imagesInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.807975"^^xsd:dateTime ;
            prov:entity id:cb4c5d07-5b7e-435f-882c-afe14e061f4b ;
            prov:hadRole wf:main_measureInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.108679"^^xsd:dateTime ;
            prov:entity id:_1b6185c0-b83d-431b-a2ba-7c2b026b1823 ;
            prov:hadRole wf:main_EchoProcess_geometryInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.812817"^^xsd:dateTime ;
            prov:entity id:_8edd155f-17b1-48d6-ae93-bad0390c9ef3 ;
            prov:hadRole wf:main_geometryInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.106052"^^xsd:dateTime ;
            prov:entity id:fc017dcf-09ec-4cbf-81ac-741b5a61b482 ;
            prov:hadRole wf:main_EchoProcess_measureInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:11.401851"^^xsd:dateTime ;
            prov:entity id:fbb085ae-d3ad-4639-a448-b01188f1ce9f ;
            prov:hadRole wf:main_EchoProcess_featureCollectionInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.813646"^^xsd:dateTime ;
            prov:entity id:d4ac4ab8-25a3-4412-82b6-07b92da98795 ;
            prov:hadRole wf:main_boundingBoxInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.807817"^^xsd:dateTime ;
            prov:entity data:_0cf60d40470fde378076afacf5812f961208a018 ;
            prov:hadRole wf:main_stringInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.809545"^^xsd:dateTime ;
            prov:entity id:c68b1b94-7f88-4cda-87da-f5e68beabe42 ;
            prov:hadRole wf:main_arrayInput ],
        [ a prov:Usage ;
            prov:atTime "2026-01-15T16:46:10.810650"^^xsd:dateTime ;
            prov:entity id:_5f78096f-fce2-49b1-aa6d-941927d15dcc ;
            prov:hadRole wf:main_complexObjectInput ] ;
    prov:startedAtTime "2026-01-15T16:46:10.775907"^^xsd:dateTime .


```

## Schema

```yaml
definitions:
  DateTime:
    $id: '#/definitions/DateTime'
    type: string
    format: date-time
  QualifiedName:
    $id: '#/definitions/QualifiedName'
    type: string
    title: The QualifiedName Schema
    default: ''
    pattern: (^[A-Za-z0-9_]+:)?(.*)$
  QualifiedName+:
    $id: '#/definitions/QualifiedName+'
    oneOf:
    - $ref: '#/definitions/QualifiedName'
    - type: array
      items:
        $ref: '#/definitions/QualifiedName'
  non_prov_properties:
    $id: '#/definitions/non_prov_properties'
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$: {}
  typed_value:
    type: object
    required:
    - '@value'
    - '@type'
    properties:
      '@value':
        type: string
      '@type':
        type: string
    additionalProperties: false
  lang_string:
    type: object
    required:
    - '@value'
    properties:
      '@value':
        type: string
      '@language':
        type: string
    additionalProperties: false
  ArrayOfValues:
    $id: '#/definitions/ArrayOfValues'
    type: array
    items:
      anyOf:
      - $ref: '#/definitions/QualifiedName'
      - $ref: '#/definitions/typed_value'
      - $ref: '#/definitions/lang_string'
  ArrayOfLabelValues:
    $id: '#/definitions/ArrayOfLabelValues'
    type: array
    items:
      $ref: '#/definitions/lang_string'
  Context:
    $id: '#/definitions/Context'
    type: array
    title: The @context Schema
    items:
      oneOf:
      - type: string
        format: uri
      - type: object
        title: The Items Schema
        additionalProperties:
          type: string
  prov:StatementOrBundle:
    oneOf:
    - $ref: '#/definitions/prov:Statement'
    - $ref: '#/definitions/prov:Bundle'
  prov:Statement:
    oneOf:
    - $ref: '#/definitions/prov:Entity'
    - $ref: '#/definitions/prov:Activity'
    - $ref: '#/definitions/prov:Agent'
    - $ref: '#/definitions/prov:Usage'
    - $ref: '#/definitions/prov:Generation'
    - $ref: '#/definitions/prov:Attribution'
    - $ref: '#/definitions/prov:Association'
    - $ref: '#/definitions/prov:Delegation'
    - $ref: '#/definitions/prov:Invalidation'
    - $ref: '#/definitions/prov:Start'
    - $ref: '#/definitions/prov:End'
    - $ref: '#/definitions/prov:Derivation'
    - $ref: '#/definitions/prov:Alternate'
    - $ref: '#/definitions/prov:Specialization'
    - $ref: '#/definitions/prov:Membership'
    - $ref: '#/definitions/prov:Influence'
    - $ref: '#/definitions/prov:Communication'
  prov:Entity:
    type: object
    required:
    - '@type'
    - '@id'
    properties:
      '@type':
        pattern: Entity
      '@id':
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      value:
        $ref: '#/definitions/ArrayOfValues'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Agent:
    type: object
    required:
    - '@type'
    - '@id'
    properties:
      '@type':
        pattern: Agent
      '@id':
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Activity:
    type: object
    required:
    - '@type'
    - '@id'
    properties:
      '@type':
        pattern: Activity
      '@id':
        $ref: '#/definitions/QualifiedName'
      startTime:
        $ref: '#/definitions/DateTime'
      endTime:
        $ref: '#/definitions/DateTime'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Usage:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Usage
      '@id':
        $ref: '#/definitions/QualifiedName'
      entity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#entity
        x-jsonld-type: '@id'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      time:
        $ref: '#/definitions/DateTime'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      role:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#hadRole
        x-jsonld-type: '@id'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Generation:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Generation
      '@id':
        $ref: '#/definitions/QualifiedName'
      entity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#entity
        x-jsonld-type: '@id'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      time:
        $ref: '#/definitions/DateTime'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      role:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#hadRole
        x-jsonld-type: '@id'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Invalidation:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Invalidation
      '@id':
        $ref: '#/definitions/QualifiedName'
      entity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#entity
        x-jsonld-type: '@id'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      time:
        $ref: '#/definitions/DateTime'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      role:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#hadRole
        x-jsonld-type: '@id'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Start:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Start
      '@id':
        $ref: '#/definitions/QualifiedName'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      starter:
        $ref: '#/definitions/QualifiedName'
      trigger:
        $ref: '#/definitions/QualifiedName'
      time:
        $ref: '#/definitions/DateTime'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      role:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#hadRole
        x-jsonld-type: '@id'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:End:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: End
      '@id':
        $ref: '#/definitions/QualifiedName'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      ender:
        $ref: '#/definitions/QualifiedName'
      trigger:
        $ref: '#/definitions/QualifiedName'
      time:
        $ref: '#/definitions/DateTime'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      role:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#hadRole
        x-jsonld-type: '@id'
      location:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#atLocation
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Attribution:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Attribution
      '@id':
        $ref: '#/definitions/QualifiedName'
      entity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#entity
        x-jsonld-type: '@id'
      agent:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#agent
        x-jsonld-type: '@id'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Association:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Association
      '@id':
        $ref: '#/definitions/QualifiedName'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      agent:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#agent
        x-jsonld-type: '@id'
      plan:
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      role:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/ns/prov#hadRole
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Delegation:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Delegation
      '@id':
        $ref: '#/definitions/QualifiedName'
      delegate:
        $ref: '#/definitions/QualifiedName'
      responsible:
        $ref: '#/definitions/QualifiedName'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Derivation:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Derivation
      '@id':
        $ref: '#/definitions/QualifiedName'
      activity:
        $ref: '#/definitions/QualifiedName'
        x-jsonld-id: http://www.w3.org/ns/prov#activity
        x-jsonld-type: '@id'
      generation:
        $ref: '#/definitions/QualifiedName'
      usage:
        $ref: '#/definitions/QualifiedName'
      generatedEntity:
        $ref: '#/definitions/QualifiedName'
      usedEntity:
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Alternate:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Alternate
      '@id':
        $ref: '#/definitions/QualifiedName'
      alternate1:
        $ref: '#/definitions/QualifiedName'
      alternate2:
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Specialization:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Specialization
      '@id':
        $ref: '#/definitions/QualifiedName'
      generalEntity:
        $ref: '#/definitions/QualifiedName'
      specificEntity:
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Membership:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Membership
      '@id':
        $ref: '#/definitions/QualifiedName'
      entity:
        $ref: '#/definitions/QualifiedName+'
        x-jsonld-id: http://www.w3.org/ns/prov#entity
        x-jsonld-type: '@id'
      collection:
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Influence:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Influence
      '@id':
        $ref: '#/definitions/QualifiedName'
      influencer:
        $ref: '#/definitions/QualifiedName'
      influencee:
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Communication:
    type: object
    required:
    - '@type'
    properties:
      '@type':
        pattern: Communication
      '@id':
        $ref: '#/definitions/QualifiedName'
      informant:
        $ref: '#/definitions/QualifiedName'
      informed:
        $ref: '#/definitions/QualifiedName'
      type:
        $ref: '#/definitions/ArrayOfValues'
        x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
        x-jsonld-type: '@id'
      label:
        $ref: '#/definitions/ArrayOfLabelValues'
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    patternProperties:
      ^[A-Za-z0-9_]+:(.*)$:
        $ref: '#/definitions/ArrayOfValues'
    additionalProperties: false
  prov:Bundle:
    type: object
    required:
    - '@type'
    - '@id'
    - '@graph'
    - '@context'
    properties:
      '@type':
        pattern: Bundle
      '@id':
        $ref: '#/definitions/QualifiedName'
      '@context':
        $ref: '#/definitions/Context'
      '@graph':
        type: array
        items:
          $ref: '#/definitions/prov:Statement'
    additionalProperties: false
  prov:Document:
    type: object
    required:
    - '@context'
    - '@graph'
    properties:
      '@type':
        pattern: Document
      '@context':
        $ref: '#/definitions/Context'
      '@graph':
        type: array
        items:
          $ref: '#/definitions/prov:StatementOrBundle'
    additionalProperties: false
$schema: http://json-schema.org/draft-07/schema#
$id: https://openprovenance.org/prov-jsonld/schema.json
$ref: '#/definitions/prov:Document'
x-jsonld-extra-terms:
  role:
    x-jsonld-id: http://www.w3.org/ns/prov#hadRole
    x-jsonld-type: '@id'
  type:
    x-jsonld-id: http://www.w3.org/1999/02/22-rdf-syntax-ns#type
    x-jsonld-type: '@id'
  label: http://www.w3.org/2000/01/rdf-schema#label
  location:
    x-jsonld-id: http://www.w3.org/ns/prov#atLocation
    x-jsonld-type: '@id'
  entity:
    x-jsonld-id: http://www.w3.org/ns/prov#entity
    x-jsonld-type: '@id'
  activity:
    x-jsonld-id: http://www.w3.org/ns/prov#activity
    x-jsonld-type: '@id'
  agent:
    x-jsonld-id: http://www.w3.org/ns/prov#agent
    x-jsonld-type: '@id'
  Activity:
    x-jsonld-id: http://www.w3.org/ns/prov#Activity
    x-jsonld-context:
      startTime:
        '@id': http://www.w3.org/ns/prov#startedAtTime
        '@type': http://www.w3.org/2001/XMLSchema#dateTime
      endTime:
        '@id': http://www.w3.org/ns/prov#endedAtTime
        '@type': http://www.w3.org/2001/XMLSchema#dateTime
  Document: https://openprovenance.org/ns/provext#Document
  Bundle: http://www.w3.org/ns/prov#Bundle
  Entity:
    x-jsonld-id: http://www.w3.org/ns/prov#Entity
    x-jsonld-context:
      value:
        '@id': http://www.w3.org/ns/prov#value
  Agent:
    x-jsonld-id: http://www.w3.org/ns/prov#Agent
    x-jsonld-context: {}
  Delegation:
    x-jsonld-id: http://www.w3.org/ns/prov#Delegation
    x-jsonld-context:
      responsible:
        '@id': http://www.w3.org/ns/prov#agent
        '@type': '@id'
      delegate:
        '@reverse': prov:qualifiedDelegation
        '@type': '@id'
      activity:
        '@id': http://www.w3.org/ns/prov#hadActivity
        '@type': '@id'
  Usage:
    x-jsonld-id: http://www.w3.org/ns/prov#Usage
    x-jsonld-context:
      activity:
        '@reverse': prov:qualifiedUsage
        '@type': '@id'
      time:
        '@id': http://www.w3.org/ns/prov#atTime
        '@type': http://www.w3.org/2001/XMLSchema#dateTime
  Generation:
    x-jsonld-id: http://www.w3.org/ns/prov#Generation
    x-jsonld-context:
      entity:
        '@reverse': prov:qualifiedGeneration
        '@type': '@id'
      time:
        '@id': http://www.w3.org/ns/prov#atTime
        '@type': http://www.w3.org/2001/XMLSchema#dateTime
  Invalidation:
    x-jsonld-id: http://www.w3.org/ns/prov#Invalidation
    x-jsonld-context:
      entity:
        '@reverse': prov:qualifiedInvalidation
        '@type': '@id'
      time:
        '@id': http://www.w3.org/ns/prov#atTime
        '@type': http://www.w3.org/2001/XMLSchema#dateTime
  Attribution:
    x-jsonld-id: http://www.w3.org/ns/prov#Attribution
    x-jsonld-context:
      entity:
        '@reverse': prov:qualifiedAttribution
        '@type': '@id'
  Association:
    x-jsonld-id: http://www.w3.org/ns/prov#Association
    x-jsonld-context:
      activity:
        '@reverse': prov:qualifiedAssociation
        '@type': '@id'
      plan:
        '@id': http://www.w3.org/ns/prov#hadPlan
        '@type': '@id'
  Communication:
    x-jsonld-id: http://www.w3.org/ns/prov#Communication
    x-jsonld-context:
      informed:
        '@reverse': prov:qualifiedCommunication
        '@type': '@id'
      informant:
        '@id': http://www.w3.org/ns/prov#activity
        '@type': '@id'
  Influence:
    x-jsonld-id: http://www.w3.org/ns/prov#Influence
    x-jsonld-context:
      influencee:
        '@reverse': prov:qualifiedInfluence
        '@type': '@id'
      influencer:
        '@id': http://www.w3.org/ns/prov#influencer
        '@type': '@id'
  Derivation:
    x-jsonld-id: http://www.w3.org/ns/prov#Derivation
    x-jsonld-context:
      generatedEntity:
        '@reverse': prov:qualifiedDerivation
        '@type': '@id'
      usedEntity:
        '@id': http://www.w3.org/ns/prov#entity
        '@type': '@id'
      generation:
        '@id': http://www.w3.org/ns/prov#hadGeneration
        '@type': '@id'
      activity:
        '@id': http://www.w3.org/ns/prov#hadActivity
        '@type': '@id'
      usage:
        '@id': http://www.w3.org/ns/prov#hadUsage
        '@type': '@id'
  Start:
    x-jsonld-id: http://www.w3.org/ns/prov#Start
    x-jsonld-context:
      activity:
        '@reverse': prov:qualifiedStart
        '@type': '@id'
      trigger:
        '@id': http://www.w3.org/ns/prov#entity
        '@type': '@id'
      starter:
        '@id': http://www.w3.org/ns/prov#hadActivity
        '@type': '@id'
      time:
        '@id': http://www.w3.org/ns/prov#atTime
        '@type': http://www.w3.org/2001/XMLSchema#dateTime
  End:
    x-jsonld-id: http://www.w3.org/ns/prov#End
    x-jsonld-context:
      activity:
        '@reverse': prov:qualifiedEnd
        '@type': '@id'
      trigger:
        '@id': http://www.w3.org/ns/prov#entity
        '@type': '@id'
      ender:
        '@id': http://www.w3.org/ns/prov#hadActivity
        '@type': '@id'
      time:
        '@id': http://www.w3.org/ns/prov#atTime
        '@type': http://www.w3.org/2001/XMLSchema#dateTime
  Specialization:
    x-jsonld-id: https://openprovenance.org/ns/provext#Specialization
    x-jsonld-context:
      specificEntity:
        '@reverse': provext:qualifiedSpecialization
        '@type': '@id'
      generalEntity:
        '@id': https://openprovenance.org/ns/provext#generalEntity
        '@type': '@id'
  Membership:
    x-jsonld-id: https://openprovenance.org/ns/provext#Membership
    x-jsonld-context:
      collection:
        '@reverse': provext:qualifiedMembership
        '@type': '@id'
      entity:
        '@id': https://openprovenance.org/ns/provext#member
        '@type': '@id'
  Alternate:
    x-jsonld-id: https://openprovenance.org/ns/provext#Alternate
    x-jsonld-context:
      alternate1:
        '@reverse': provext:qualifiedAlternate
        '@type': '@id'
      alternate2:
        '@id': https://openprovenance.org/ns/provext#alternate
        '@type': '@id'
x-jsonld-prefixes:
  prov: http://www.w3.org/ns/prov#
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  xsd: http://www.w3.org/2001/XMLSchema#
  provext: https://openprovenance.org/ns/provext#

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-prov-jsonld-alt/build/annotated/ogc-utils/prov/w3c-prov-jsonld/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-prov-jsonld-alt/build/annotated/ogc-utils/prov/w3c-prov-jsonld/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "role": {
      "@id": "prov:hadRole",
      "@type": "@id"
    },
    "type": {
      "@id": "rdf:type",
      "@type": "@id"
    },
    "label": "rdfs:label",
    "location": {
      "@id": "prov:atLocation",
      "@type": "@id"
    },
    "entity": {
      "@id": "prov:entity",
      "@type": "@id"
    },
    "activity": {
      "@id": "prov:activity",
      "@type": "@id"
    },
    "agent": {
      "@id": "prov:agent",
      "@type": "@id"
    },
    "Activity": {
      "@id": "prov:Activity",
      "@context": {
        "startTime": {
          "@id": "prov:startedAtTime",
          "@type": "xsd:dateTime"
        },
        "endTime": {
          "@id": "prov:endedAtTime",
          "@type": "xsd:dateTime"
        }
      }
    },
    "Document": "provext:Document",
    "Bundle": "prov:Bundle",
    "Entity": {
      "@id": "prov:Entity",
      "@context": {
        "value": "prov:value"
      }
    },
    "Agent": "prov:Agent",
    "Delegation": {
      "@id": "prov:Delegation",
      "@context": {
        "responsible": {
          "@id": "prov:agent",
          "@type": "@id"
        },
        "delegate": {
          "@reverse": "prov:qualifiedDelegation",
          "@type": "@id"
        },
        "activity": {
          "@id": "prov:hadActivity",
          "@type": "@id"
        }
      }
    },
    "Usage": {
      "@id": "prov:Usage",
      "@context": {
        "activity": {
          "@reverse": "prov:qualifiedUsage",
          "@type": "@id"
        },
        "time": {
          "@id": "prov:atTime",
          "@type": "xsd:dateTime"
        }
      }
    },
    "Generation": {
      "@id": "prov:Generation",
      "@context": {
        "entity": {
          "@reverse": "prov:qualifiedGeneration",
          "@type": "@id"
        },
        "time": {
          "@id": "prov:atTime",
          "@type": "xsd:dateTime"
        }
      }
    },
    "Invalidation": {
      "@id": "prov:Invalidation",
      "@context": {
        "entity": {
          "@reverse": "prov:qualifiedInvalidation",
          "@type": "@id"
        },
        "time": {
          "@id": "prov:atTime",
          "@type": "xsd:dateTime"
        }
      }
    },
    "Attribution": {
      "@id": "prov:Attribution",
      "@context": {
        "entity": {
          "@reverse": "prov:qualifiedAttribution",
          "@type": "@id"
        }
      }
    },
    "Association": {
      "@id": "prov:Association",
      "@context": {
        "activity": {
          "@reverse": "prov:qualifiedAssociation",
          "@type": "@id"
        },
        "plan": {
          "@id": "prov:hadPlan",
          "@type": "@id"
        }
      }
    },
    "Communication": {
      "@id": "prov:Communication",
      "@context": {
        "informed": {
          "@reverse": "prov:qualifiedCommunication",
          "@type": "@id"
        },
        "informant": {
          "@id": "prov:activity",
          "@type": "@id"
        }
      }
    },
    "Influence": {
      "@id": "prov:Influence",
      "@context": {
        "influencee": {
          "@reverse": "prov:qualifiedInfluence",
          "@type": "@id"
        },
        "influencer": {
          "@id": "prov:influencer",
          "@type": "@id"
        }
      }
    },
    "Derivation": {
      "@id": "prov:Derivation",
      "@context": {
        "generatedEntity": {
          "@reverse": "prov:qualifiedDerivation",
          "@type": "@id"
        },
        "usedEntity": {
          "@id": "prov:entity",
          "@type": "@id"
        },
        "generation": {
          "@id": "prov:hadGeneration",
          "@type": "@id"
        },
        "activity": {
          "@id": "prov:hadActivity",
          "@type": "@id"
        },
        "usage": {
          "@id": "prov:hadUsage",
          "@type": "@id"
        }
      }
    },
    "Start": {
      "@id": "prov:Start",
      "@context": {
        "activity": {
          "@reverse": "prov:qualifiedStart",
          "@type": "@id"
        },
        "trigger": {
          "@id": "prov:entity",
          "@type": "@id"
        },
        "starter": {
          "@id": "prov:hadActivity",
          "@type": "@id"
        },
        "time": {
          "@id": "prov:atTime",
          "@type": "xsd:dateTime"
        }
      }
    },
    "End": {
      "@id": "prov:End",
      "@context": {
        "activity": {
          "@reverse": "prov:qualifiedEnd",
          "@type": "@id"
        },
        "trigger": {
          "@id": "prov:entity",
          "@type": "@id"
        },
        "ender": {
          "@id": "prov:hadActivity",
          "@type": "@id"
        },
        "time": {
          "@id": "prov:atTime",
          "@type": "xsd:dateTime"
        }
      }
    },
    "Specialization": {
      "@id": "provext:Specialization",
      "@context": {
        "specificEntity": {
          "@reverse": "provext:qualifiedSpecialization",
          "@type": "@id"
        },
        "generalEntity": {
          "@id": "provext:generalEntity",
          "@type": "@id"
        }
      }
    },
    "Membership": {
      "@id": "provext:Membership",
      "@context": {
        "collection": {
          "@reverse": "provext:qualifiedMembership",
          "@type": "@id"
        },
        "entity": {
          "@id": "provext:member",
          "@type": "@id"
        }
      }
    },
    "Alternate": {
      "@id": "provext:Alternate",
      "@context": {
        "alternate1": {
          "@reverse": "provext:qualifiedAlternate",
          "@type": "@id"
        },
        "alternate2": {
          "@id": "provext:alternate",
          "@type": "@id"
        }
      }
    },
    "prov": "http://www.w3.org/ns/prov#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "provext": "https://openprovenance.org/ns/provext#",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-prov-jsonld-alt/build/annotated/ogc-utils/prov/w3c-prov-jsonld/context.jsonld)

## Sources

* [The PROV-JSONLD Serialization](https://www.w3.org/submissions/2024/SUBM-prov-jsonld-20240825/)
* [OGC API - Processes - Part 5: Provenance (registers `application/ld+json` for PROV-JSONLD)](https://docs.ogc.org/DRAFTS/26-038.html)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-prov-jsonld-alt](https://github.com/ogcincubator/bblocks-prov-jsonld-alt)
* Path: `_sources/prov/w3c-prov-jsonld`

