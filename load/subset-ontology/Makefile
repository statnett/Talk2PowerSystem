# GraphDB query and format commands
# Query GraphDB and save results as TTL
all: ontology-formatted.ttl ontology-lite.ttl

ontology-lite.ttl: ontology-query.rq
	curl -X POST \
		-H "Content-Type: application/sparql-query" \
		-H "Accept: application/x-turtle" \
		--data-binary @ontology-query.rq \
		"https://cim.ontotext.com/graphdb/repositories/nordic44" \
		> ontology-lite.ttl

# Format the TTL file using owl-toolkit
ontology-formatted.ttl: ontology-lite.ttl
	echo "formatting using owl write" ;
	owl write ontology-lite.ttl > ontology-formatted.ttl