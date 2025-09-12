PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
insert {
    graph <https://cim.ucaiug.io/qudt> {
        ?qudt ?p ?o .
    }
} where {
    ?s skos:exactMatch ?qudt .
    filter not exists {
        ?qudt a []
    }
    filter(contains(str(?qudt),"http://qudt.org/vocab"))
    service <https://www.qudt.org/fuseki/qudt/sparql> {
        ?qudt ?p ?o .
    }
}