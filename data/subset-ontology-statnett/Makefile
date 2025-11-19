PRETTY = ontology_ems_cim15_pretty.ttl ontology_sa_cim16_pretty.ttl ontology_kam_cim17_pretty.ttl

all: $(PRETTY) check statnett-terms-MISSING.txt statnett-cim15-MISSING.txt statnett-cim15-extra.ttl

%_pretty.ttl: prefixes.ttl %.ttl
	cat $^ > temp.ttl
	owl.bat write --useCommaByDefault temp.ttl $@
	rm temp.ttl

check: $(PRETTY)
	@echo "Should find no matches and return Error 1 (ignored)"
	-grep "<ht" $^ | grep -v "@prefix"

statnett-terms-MISSING.txt: $(PRETTY)
	grep -h MISSING $^ | sort | uniq > $@

statnett-cim15-MISSING.txt: ontology_ems_cim15_pretty.ttl
	grep -h MISSING $^ | sort | uniq > $@

statnett-cim15-extra.ttl: statnett-cim15-extra.rdf
	riot.bat --formatted ttl $^ > temp.ttl
	owl.bat write --useCommaByDefault temp.ttl $@
	rm temp.ttl
