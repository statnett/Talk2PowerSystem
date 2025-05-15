# Ontology subsetting
Issue: [#96](https://github.com/statnett/Talk2PowerSystem_PM/issues/96)

Query to generate ontology: [ontology-query.rq](ontology-query.rq)

Query to check for props without definitions:

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE
{
    {
        SELECT DISTINCT ?x {
            {
                [] ?x []
            } UNION {
                [] a ?x
            }
        }
    }
    VALUES ?p_def {
        rdfs:label
        rdf:type
        rdfs:comment
    }
    FILTER NOT EXISTS {?x ?p_def []}
}   order by ?x
```

Some Issues:
common ontologies not loaded `dcat`, `dct`, `vann`, `skos`, `qudt`, `rdfs`, `rdfg`?, `owl`?