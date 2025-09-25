PREFIX cim: <https://cim.ucaiug.io/ns#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>

DELETE WHERE {
  ?x a cim:PositionPoint ;
    ?p ?o .
};

DELETE {?s ?p ?o}
WHERE {
  VALUES ?p {geo:asGML geo:asGeoJSON}
  ?s ?p ?o .
};
