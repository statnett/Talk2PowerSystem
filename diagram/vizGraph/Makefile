ENDPOINT   = https://cim.ontotext.com/graphdb/rest/explore-graph/
CREDS_FILE = creds.txt # expects it formatted as user:password no new line
TTL        = diagrams.ttl diagramConfigs.ttl
TRIG       = $(TTL:ttl=trig)

all: $(TRIG)

ttl: $(TTL)

%.trig: %-header.trig  %.ttl diagrams-footer.trig
	cat $*.ttl | grep -v '^@prefix' | cat $*-header.trig - diagrams-footer.trig > $@

%.ttl: %.json %.rq
	sparql-anything -v location=$*.json -o $*.ttl -q $*.rq

get:
	curl --anyauth   -s -u "$$(cat $(CREDS_FILE))" "$(ENDPOINT)/saved" --header "x-graphdb-repository: cim" -o diagrams.json
	curl --anyauth   -s -u "$$(cat $(CREDS_FILE))" "$(ENDPOINT)/config" --header "x-graphdb-repository: cim" -o diagramConfigs.json	