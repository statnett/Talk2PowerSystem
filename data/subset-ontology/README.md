# Ontology Subsetting and GraphQL Schema Generation


## Ontology Subsetting
Issues:
- [Ontology subsetting and presentation to LLM #96](https://github.com/statnett/Talk2PowerSystem_PM/issues/96).
- [keep cims:multiplicity in ontology subsetting #173](https://github.com/statnett/Talk2PowerSystem_PM/issues/173)
- [exclude `Model, dct:resource11` from subset #175](https://github.com/statnett/Talk2PowerSystem_PM/issues/175)
- [ontology subset is missing enum values #181](https://github.com/statnett/Talk2PowerSystem_PM/issues/181)
- [collect and display component information #197](https://github.com/statnett/Talk2PowerSystem_PM/issues/197)
- [ProdData: extract ontology subset #202](https://github.com/statnett/Talk2PowerSystem_PM/issues/202)
- [Prod Data: find classes and properties missing in ontologies #203](https://github.com/statnett/Talk2PowerSystem_PM/issues/203)
- [consider removing external terms from subset (dct, dcat, etc) #205](https://github.com/statnett/Talk2PowerSystem_PM/issues/205)
- [add a cims:MISSING to terms used but not defined #206](https://github.com/statnett/Talk2PowerSystem_PM/issues/206)


The complete set of CIM, CGMES and NC ontologies have 900 classes and 5500 properties.
(Many of these terms are defined up to 20 times across the different CIM profiles, but luckily the definitions are consistent, so they don't result in duplicate terms).
This is a huge amount of info, so the LLM gets confused if we present all of it.

The purpose of Ontology Subsetting is to make it easier for the LLM to understand it.
See also [Blog Ontology Simplification for LLM](https://github.com/statnett/Talk2PowerSystem/wiki/Blog-Ontology-Simplification-for-LLM)
* TODO: copy all details from #96 into the description below.
* The input consists of CIM and NC ontologies from [Inst4CIM-KG/rdfs-improved](https://github.com/Sveino/Inst4CIM-KG/blob/develop/rdfs-improved/)
* TODO: add info about `owl:imports` (#197)
* The result is in [cim-subset-pretty.ttl](cim-subset-pretty.ttl). 
* TODO: add info about `ontology-record`
* We use [ontology-query.rq](ontology-query.rq) to generate a `ttl` file, 
  which is then prettified using [owl atextor tools: owl-cli and turtle-formatter](https://github.com/Sveino/Inst4CIM-KG/tree/develop/rdfs-improved#atextor-tools-owl-cli-and-turtle-formatter)
* For terms that are used but not defined in the base ontologies, we emit `a cims:MISSING`
* See [Makefile](Makefile) 
* For `make` to work, `owl` should invoke `owl-cli-snapshot.jar` with the args
  
# GraphQL Schema Generation
We use [owl2soml](https://github.com/VladimirAlexiev/soml/tree/master/owl2soml) to generate a SOML schema for GraphQL querying.
```
perl -S owl2soml.pl -id cim -label CIM -name cim:identifiedObject.name -super 1 -string 2 cim-subset-pretty-ontology.ttl > cim-subset-pretty-ontology.yaml
```

Options used:
- `-id cim -label CIM`: set schema id and label
- `-name identifiedObject.name`: refer to this often used prop simply as `name`
- `-super 1` generates abstract interfaces for each superclass, eg `IdentifiedObjectInterface` is superclass of pretty much every CIM class
- `-string 2` downgrades langString to string (actually CIM data doesn't use langString, only CIM ontologies use it)

TODO: [#173 keep cims:multiplicity in ontology subsetting](https://github.com/statnett/Talk2PowerSystem_PM/issues/173) 

## Generation warnings
It gives the following warnings, but they are harmless (`md:Model` should not be used anyway).
```
Prop dcat:temporalResolution uses unsupported datatype xsd:duration, ignored
Found multiple ranges for prop dct:resource1, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:spatial, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:resource2, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dcat:isVersionOf, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:resource4, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:resource11, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:resource3, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:accessRights, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:resource13, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dcat:hasVersion, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop prov:wasGeneratedBy, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:license, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:references, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:resource10, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop prov:entity, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:conformsTo, using only the first one: dcat:Dataset, md:Model
Found multiple ranges for prop dct:type, using only the first one: dcat:Dataset, md:Model
```

## Import errors
When we import the SOML schema at https://cim.ontotext.com/graphdb/graphql/endpoints, we get this GraphQL endpoint creation report

These are unimportant because `md:Model` should not be used, and  `dct:resource11` (intended to be `inverseOf: dct:publisher`) is defective (wrong name).
But they are treated as errors, so they preclude loading the schema
```
ERROR: Property 'dct:resource11' refers to an undefined 'inverseOf: dct:publisher' in 'range: dcat:Dataset'
ERROR: Property 'md:Model.dcat:hasVersion' is inverse property of 'dcat:Dataset.dcat:isVersionOf', but the range of 'dcat:Dataset.dcat:isVersionOf' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dcat:isVersionOf' is inverse property of 'dcat:Dataset.dcat:hasVersion', but the range of 'dcat:Dataset.dcat:hasVersion' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:accessRights' is inverse property of 'dcat:Dataset.dct:resource1', but the range of 'dcat:Dataset.dct:resource1' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:conformsTo' is inverse property of 'dcat:Dataset.dct:resource2', but the range of 'dcat:Dataset.dct:resource2' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:license' is inverse property of 'dcat:Dataset.dct:resource3', but the range of 'dcat:Dataset.dct:resource3' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:publisher' is inverse property of 'md:Model.dct:resource11', but the range of 'md:Model.dct:resource11' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:references' is inverse property of 'dcat:Dataset.dct:resource13', but the range of 'dcat:Dataset.dct:resource13' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:resource1' is inverse property of 'dcat:Dataset.dct:accessRights', but the range of 'dcat:Dataset.dct:accessRights' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:resource10' is inverse property of 'dcat:Dataset.dct:spatial', but the range of 'dcat:Dataset.dct:spatial' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:resource13' is inverse property of 'dcat:Dataset.dct:references', but the range of 'dcat:Dataset.dct:references' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:resource2' is inverse property of 'dcat:Dataset.dct:conformsTo', but the range of 'dcat:Dataset.dct:conformsTo' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:resource3' is inverse property of 'dcat:Dataset.dct:license', but the range of 'dcat:Dataset.dct:license' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:resource4' is inverse property of 'dcat:Dataset.dct:type', but the range of 'dcat:Dataset.dct:type' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:spatial' is inverse property of 'dcat:Dataset.dct:resource10', but the range of 'dcat:Dataset.dct:resource10' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.dct:type' is inverse property of 'dcat:Dataset.dct:resource4', but the range of 'dcat:Dataset.dct:resource4' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.prov:entity' is inverse property of 'dcat:Dataset.prov:wasGeneratedBy', but the range of 'dcat:Dataset.prov:wasGeneratedBy' is 'dcat:Dataset', which is not a superclass of 'md:Model'
ERROR: Property 'md:Model.prov:wasGeneratedBy' is inverse property of 'dcat:Dataset.prov:entity', but the range of 'dcat:Dataset.prov:entity' is 'dcat:Dataset', which is not a superclass of 'md:Model'
```
- Task [#175 exclude Model, dct:resource11 from subset](https://github.com/statnett/Talk2PowerSystem_PM/issues/175)
- Hotfixed in `cim-subset-hotfixed.ttl`

We need to fix these (by assigning domain/range) so we can use them in querying
```
ERROR: Property 'cimr:hasPart' refers to an undefined 'inverseOf: cimr:isPart' in 'range: iri'
ERROR: Property 'cimr:hasPartTransitive' refers to an undefined 'inverseOf: cimr:isPartTransitive' in 'range: iri'
ERROR: Property 'cimr:isPart' refers to an undefined 'inverseOf: cimr:hasPart' in 'range: iri'
ERROR: Property 'cimr:isPartTransitive' refers to an undefined 'inverseOf: cimr:hasPartTransitive' in 'range: iri'
ERROR: Property 'cimr:equipment_Terminals' refers to an undefined 'inverseOf: cimr:terminal.Equipment' in 'range: iri'
ERROR: Property 'cimr:terminal_Equipment' refers to an undefined 'inverseOf: cimr:equipment.Terminals' in 'range: iri'
```
- Added domain/range to `cimr.ttl`
- Concatenated the same to the end of  `cim-subset-hotfixed.ttl`
