Issue: [#96](https://github.com/statnett/Talk2PowerSystem_PM/issues/96)

# Ontology subsetting

Subsetting of the ontology for the purpose of informing the LLM.

* Result is in [cim-subset-pretty.ttl](cim-subset-pretty.ttl)
* We use [ontology-query.rq](ontology-query.rq) to generate a `ttl` file, 
  which is then prettified using [owl atextor tools: owl-cli and turtle-formatter](https://github.com/Sveino/Inst4CIM-KG/tree/develop/rdfs-improved#atextor-tools-owl-cli-and-turtle-formatter)
* See [Makefile](Makefile) 
* For `make` to work `owl` should invoke `owl-cli-snapshot.jar` with the args
  