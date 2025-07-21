PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX cim: <https://cim.ucaiug.io/ns#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
insert {
  graph ?g {
      ?psr a geo:Feature; geo:hasGeometry ?loc  .
      ?loc a geo:Geometry; geo:asWKT ?wkt .
  }
}
where
{
    select ?psr ?loc ?g (strdt(concat(?type,"(",group_concat(concat(str(?x)," ",str(?y)); separator=", "),")"),geo:wktLiteral) as ?wkt)  where {
        graph ?g {?point cim:PositionPoint.Location ?loc .}
        ?point cim:PositionPoint.Location ?loc .
        ?loc cim:Location.PowerSystemResources ?psr .
        ?point cim:PositionPoint.sequenceNumber ?seq;
        cim:PositionPoint.xPosition ?x;
        cim:PositionPoint.yPosition ?y;
        bind(if(exists{
                    ?loc ^cim:PositionPoint.Location/cim:PositionPoint.sequenceNumber 2
                },"LINESTRING","POINT") as ?type)
    } group by ?g ?psr ?loc ?type order by ?seq
}