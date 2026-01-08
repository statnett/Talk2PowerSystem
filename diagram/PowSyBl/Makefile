TTL = $(wildcard queries/*.ttl)

all: diagrams.trig diagrams.tsv diagrams-fixed.trig diagrams-fixed.tsv

diagrams.trig: $(TTL) | diagrams-header.trig diagrams-footer.trig
	cat $^ | grep -v '^@prefix' | cat diagrams-header.trig - diagrams-footer.trig > $@

diagrams-fixed.trig: diagrams-delete.ru diagrams.trig
	update.bat --update=diagrams-delete.ru --data=diagrams.trig --dump > diagrams-fixed.trig
	
diagrams.tsv: queries/diagrams.rq diagrams.trig
	arq.bat --query=queries/diagrams.rq --data=diagrams.trig --results=tsv > diagrams.tsv

diagrams-fixed.tsv: queries/diagrams.rq diagrams-fixed.trig
	arq.bat --query=queries/diagrams.rq --data=diagrams-fixed.trig --results=tsv > diagrams-fixed.tsv
