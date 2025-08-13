# GraphDB query and format commands
# Query GraphDB and save results as TTL

all: cim-subset.ttl cim-subset-pretty.ttl cim-subset-pretty-hotfixed.ttl cim-subset-pretty-ontology.ttl cim-subset-pretty-ontology.yaml

cim-subset.ttl: ontology-query.rq
	curl -X POST \
		-H "Content-Type: application/sparql-query" \
		-H "Accept: application/x-turtle" \
		--data-binary @ontology-query.rq \
		"https://cim.ontotext.com/graphdb/repositories/cim" \
		> cim-subset.ttl

# Format the TTL file using owl-toolkit
cim-subset-pretty.ttl: cim-subset.ttl
	owl write --useCommaByDefault $^ $@

cim-subset-pretty-hotfixed.ttl: cim-subset-hotfixed.ttl
	owl write --useCommaByDefault $^ $@

# Add ontology record
cim-subset-pretty-ontology.ttl: cim-ontology-record.ttl cim-subset-pretty-hotfixed.ttl
	cat $^ > $@

# Generate SOML schema
cim-subset-pretty-ontology.yaml: cim-subset-pretty-ontology.ttl
	perl -S owl2soml.pl -id cim -label CIM -name identifiedObject.name -super 1 -string 2 $^ > $@
