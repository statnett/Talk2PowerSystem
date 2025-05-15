# GraphDB query and format commands
# Query GraphDB and save results as TTL
all:cim-subset.ttl cim-subset-pretty.ttl

cim-subset.ttl: ontology-query.rq
	curl -X POST \
		-H "Content-Type: application/sparql-query" \
		-H "Accept: application/x-turtle" \
		--data-binary @ontology-query.rq \
		"https://cim.ontotext.com/graphdb/repositories/nordic44" \
		> cim-subset.ttl

# Format the TTL file using owl-toolkit
cim-subset-pretty.ttl: cim-subset.ttl
	echo "formatting using owl write" ;
	owl write cim-subset.ttl > cim-subset-pretty.ttl