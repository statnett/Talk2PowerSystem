TTL = $(wildcard queries/*.ttl)

all: diagrams.ttl diagrams.tsv

diagrams.ttl: $(TTL)
	cat $^ > $@

diagrams.tsv: queries/diagrams.rq diagrams.ttl
	arq.bat --query=queries/diagrams.rq --data=diagrams.ttl --results=tsv > diagrams.tsv
