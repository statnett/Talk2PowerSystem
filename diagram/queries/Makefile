TTL = $(patsubst %.rq,%.ttl,$(wildcard PowSyBl*.rq))

all: $(TTL)
echo:
	@echo $(TTL)

# Query GraphDB and save results as TTL
%.ttl: %.rq
	curl -X POST \
	 -H "Content-Type: application/sparql-query" \
	 -H "Accept: text/turtle" \
	 --data-binary @$^ \
	 "https://cim.ontotext.com/graphdb/repositories/cim" \
	 > $@
