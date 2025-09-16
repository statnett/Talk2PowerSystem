all: ontology_ems_cim15_pretty.ttl ontology_kam_cim17_pretty.ttl ontology_sa_cim16_pretty.ttl

%_pretty.ttl: prefixes.ttl %.ttl
	cat $^ > temp.ttl
	owl.bat write --useCommaByDefault temp.ttl $@
	rm temp.ttl
