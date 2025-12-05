TTL = $(wildcard queries/*.ttl)

all: diagrams.trig diagrams.tsv

diagrams.trig: $(TTL) | diagrams-header.trig diagrams-footer.trig
	cat $^ | grep -v '^@prefix' | cat diagrams-header.trig - diagrams-footer.trig > $@

diagrams.tsv: queries/diagrams.rq diagrams.trig
	arq.bat --query=queries/diagrams.rq --data=diagrams.trig --results=tsv > diagrams.tsv
