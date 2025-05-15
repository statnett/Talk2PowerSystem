# Ontology subsetting
Issue: [#96](https://github.com/statnett/Talk2PowerSystem_PM/issues/96)

Query to generate ontology: [ontology-query.rq](ontology-query.rq)

See [Makefile](Makefile)

Query to check for props without definitions:

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX nc: <https://cim4.eu/ns/nc#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX cimex: <https://rawgit2.com/statnett/Talk2PowerSystem/main/demo1/cimex/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cim: <https://cim.ucaiug.io/ns#>
PREFIX uml: <http://iec.ch/TC57/NonStandard/UML#>
PREFIX cims: <http://iec.ch/TC57/1999/rdf-schema-extensions-19990926#>
SELECT ?x WHERE
{
    {
        SELECT DISTINCT ?x {
            {
                [] ?x []
            } UNION {
                [] a ?x
            }
        }
    } UNION {
        ?x a ?enum.
        ?enum cims:stereotype uml:enumeration
        FILTER EXISTS {
            ?thing a cim:IdentifiedObject;
            ?prop ?x
        }
    }
    FILTER NOT EXISTS {
        ?x rdfs:label [];
        rdf:type [];
        rdfs:comment []
    }
}   order by ?x
```

Some Issues:
common ontologies not loaded `dcat`, `dct`, `vann`, `skos`, `qudt`, `rdfs`, `rdfg`?, `owl`?

```bash
owl write cim-subset.ttl > cim-subset-pretty.ttl
```