PRETTY = ontology_ems_cim15_pretty.ttl ontology_kam_cim17_pretty.ttl ontology_sa_cim16_pretty.ttl

all: $(PRETTY) check statnett-terms-MISSING.txt

%_pretty.ttl: prefixes.ttl %.ttl
	cat $^ > temp.ttl
	owl.bat write --useCommaByDefault temp.ttl $@
	rm temp.ttl

check: $(PRETTY)
	@echo "Should find no matches and return Error 1 (ignored)"
	-grep "<ht" $^ | grep -v "@prefix"

statnett-terms-MISSING.txt: $(PRETTY)
	grep -h MISSING $^ | sort | uniq > $@
