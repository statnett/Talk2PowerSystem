# see https://github.com/statnett/Talk2PowerSystem_PM/issues/175

PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
delete {
    ?s ?p ?o .
}
where {
    values ?pat {
        "http://purl.org/dc/terms/Resource"
        "http://iec.ch/TC57/61970-552/ModelDescription/1#Model"
    }
    ?s ?p ?o .
    filter(
        contains(str(?s),?pat) ||
        contains(str(?p),?pat) ||
        contains(str(?o),?pat)
    )
} ;
# prop used in qudt, leading to everything from qudt being dcat:Dataset
delete where {
    dct:description rdfs:domain dcat:Dataset
};

#cleaning up labels not in en or no
delete {
    ?s ?prop ?label
}
where {
    values ?prop {
        rdfs:label
        skos:altLabel
        dct:description
    }
    ?s ?prop ?label .
    bind(lang(?label) as ?lang)
    filter(?lang)
    filter(?lang not in ("en","no"))
};