ENDPOINT = https://cim.ontotext.com/graphdb/rest/explore-graph/
TTL = diagrams.ttl diagramConfigs.ttl

all: $(TTL)

get:
	curl -s $(ENDPOINT)/saved  -o diagrams.json
	curl -s $(ENDPOINT)/config -o diagramConfigs.json

# sparql-anything is a script like this:
# java -jar .../sparql-anything-v1.0.0.jar 

%.ttl: %.json %.rq
	sparql-anything -v location=$*.rq -o $*.ttl -q $*.rq
