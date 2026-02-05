FIXME = ../../../Inst4CIM-KG/rdf-improved

all: MicroGrid-NL-MAS-EQ_diff.trig

%.trig: %.xml
	perl $(FIXME)/cim-urn-uuid.pl $^ > temp.xml
	perl $(FIXME)/cim-trig.pl temp.xml > $@
	rm temp.xml
