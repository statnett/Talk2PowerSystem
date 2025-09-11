# see https://github.com/statnett/Talk2PowerSystem_PM/issues/175

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
}