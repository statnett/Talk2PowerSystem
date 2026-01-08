
# GraphDB VizGraph Semantic Descriptions

- Task: [#293 Extract VizGraph diagram descriptions from JSON to RDF](https://github.com/statnett/Talk2PowerSystem_PM/issues/293)

## Conceptualization
- Create use cases for Configurations: some of them ("start from a node") can be invoked on any resource:
  - CIM: on `cim:PowerSystemResource` (instance node)
  - CIM Classes and Properties: on `owl:Class`
- Amend descriptions of Diagrams and DiagramConfigurations to make them best undertandable by LLM

## Get and Check
We use two REST APIs from GraphDB Workbench endpoint https://cim.ontotext.com/graphdb/rest/explore-graph/ :
- `saved`: get Diagrams
- `config`: get DiagramConfigurations 

Check that all diagrams of "admin" are configured as `shared`.

## Semantization
- Extend Ontology: add classes/enum values to the `cimd` (cim-diagrams.ttl) ontology
- Convert JSON to RDF similar to PowSyBl diagram descriptions
  - `cimd:DiagramConfiguration`: with flag `isDefault`
  - `cimd:Diagram:` saved graphs list all displayed nodes, so we'll convert that to `Diagram.PowerSystemResources`.
    But maybe we need to filter to the "most important" node(s) shown

