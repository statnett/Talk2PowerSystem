PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
insert {
    graph <https://cim.ucaiug.io/qudt> {
        ?qudt ?p ?o .
    }
}
where {
    ?s ?prop ?qudt .
    filter(contains(str(?qudt),"http://qudt.org/vocab"))
    filter not exists { ?qudt a [] }
    service <https://www.qudt.org/fuseki/qudt/sparql> {
        ?qudt ?p ?o .
    }
} ;

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
insert {
    graph <https://cim.ucaiug.io/qudt> {
        ?more_qudt ?p ?o .
    }
} where {
    {
        select distinct ?more_qudt  where {
            ?qudt ?p ?more_qudt .
            filter(?p not in(qudt:applicableUnit,rdfs:seeAlso,qudt:siExactMatch,qudt:wikidataMatch,qudt:omUnit))
            filter(contains(str(?qudt),"http://qudt.org/vocab"))
            filter(isIRI(?more_qudt))
            filter not exists {
                ?more_qudt a []
            }
        }
    }
    service <https://www.qudt.org/fuseki/qudt/sparql> {
        ?more_qudt ?p ?o .
    }
}