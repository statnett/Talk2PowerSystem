ENDPOINT = https://cim.ontotext.com/graphdb/rest/explore-graph/
TTL      = diagrams.ttl diagramConfigs.ttl
TRIG     = $(TTL:ttl=trig)

all: $(TRIG)

ttl: $(TTL)

%.trig: %-header.trig  %.ttl diagrams-footer.trig
	cat $*.ttl | grep -v '^@prefix' | cat $*-header.trig - diagrams-footer.trig > $@

# sparql-anything is a script like this:
# java -jar .../sparql-anything-v1.0.0.jar 

%.ttl: %.json %.rq
	sparql-anything -v location=$*.rq -o $*.ttl -q $*.rq

get:
	curl -s $(ENDPOINT)/saved  -o diagrams.json
	curl -s $(ENDPOINT)/config -o diagramConfigs.json
