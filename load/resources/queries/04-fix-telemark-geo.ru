PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX cim: <https://cim.ucaiug.io/ns#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>

DELETE {
    ?s ?p ?o .
}
WHERE {

    VALUES ?p
    {
       geo:asWKT
       geo:asGML
       geo:asGeoJSON
    }
    VALUES ?s {
		<urn:uuid:7d8a6fba-409a-4dc0-9b1b-f1d46668366e>
        <urn:uuid:d9dc4a4c-cf44-4025-b733-a93d9021fac3>
		<urn:uuid:f5fd7c46-d22c-4f95-8a35-cab939d38f4e>
    }
    ?s ?p ?o .
};
INSERT DATA {
	graph <urn:uuid:f1d9a88d-0ff5-4e4b-9d6a-c353fe8232c3> {
		<urn:uuid:7d8a6fba-409a-4dc0-9b1b-f1d46668366e> geo:asWKT "LINESTRING(8.7007293714585 58.414672010585065,8.7007293 58.414671999999996)"^^geo:wktLiteral .
		<urn:uuid:f5fd7c46-d22c-4f95-8a35-cab939d38f4e> geo:asWKT "POLYGON((9.641657919550369 59.17433310258693, 9.641985991575922 59.17355060327998, 9.643530912568622 59.173764569713114, 9.642862838625433 59.17453483778593, 9.641657919550369 59.17433310258693))"^^geo:wktLiteral
		.
		<urn:uuid:d9dc4a4c-cf44-4025-b733-a93d9021fac3> geo:asWKT "POINT(8.7007293,58.414672)"^^geo:wktLiteral
		.
	}
	graph <urn:uuid:971c4254-5365-4aaf-8fa6-02658b3f8e05> {
	  	<urn:uuid:971c4254-5365-4aaf-8fa6-02658b3f8e05> a dcat:Dataset;
	    	dcterms:description "Geospartial GridCapacity MAS1"@en.

	  	<urn:uuid:4e51e598-8948-4c85-b151-f44ffddc5545> a cim:Feeder, geo:Feature ;
	    	cim:IdentifiedObject.description "Sandefjord business and industry area"@en;
	    	geo:hasGeometry <urn:uuid:58aee5a8-0cd9-467e-b5e7-180ac161d9b8> .

	  	<urn:uuid:58aee5a8-0cd9-467e-b5e7-180ac161d9b8> a geo:Geometry ;
	    	geo:asWKT "POLYGON((10.229020984659712 59.24698254345179, 10.18420614097019 59.19982925336586, 10.142883363023742 59.13888033657065, 10.202442484289662 59.13758660552921, 10.276357875828012 59.16126409167293, 10.310502518638259 59.22922084872761, 10.229020984659712 59.24698254345179))"^^geo:wktLiteral .
	}
};