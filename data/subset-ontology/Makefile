# Extract subset of ontology terms in use

all: cim-subset.ttl cim-subset-pretty-ontology.ttl terms-MISSING.txt cim-subset-not-MISSING.ttl
soml: cim-subset-pretty-ontology.yaml

# Query GraphDB and save results as TTL

cim-subset.ttl: ontology-query.rq
	curl -X POST \
	 -H "Content-Type: application/sparql-query" \
	 -H "Accept: application/x-turtle" \
	 --data-binary @ontology-query.rq \
	 "https://cim.ontotext.com/graphdb/repositories/cim" \
	 > $@

terms-MISSING.txt: cim-subset.ttl
	grep MISSING $^ | sort > $@

cim-subset-not-MISSING.ttl: cim-subset.ttl
	grep -v 'MISSING \.' $^ > $@

# Add ontology record
cim-subset-ontology.ttl: cim-ontology-record.ttl cim-subset-not-MISSING.ttl
	cat $^ > $@

# Format the TTL file using owl-toolkit
cim-subset-pretty-ontology.ttl: cim-subset-ontology.ttl
	owl write --useCommaByDefault \
	 -p=owl=http://www.w3.org/2002/07/owl# \
	 -p=rdf=http://www.w3.org/1999/02/22-rdf-syntax-ns# \
	 -p=rdfs=http://www.w3.org/2000/01/rdf-schema# \
	 --subjectOrder owl:Ontology \
	 --subjectOrder rdfs:Class \
	 --subjectOrder owl:Class \
	 --subjectOrder rdf:Property \
	 --subjectOrder owl:ObjectProperty \
	 --subjectOrder owl:DatatypeProperty \
	 --subjectOrder owl:AnnotationProperty \
	 --subjectOrder owl:NamedIndividual \
	 --subjectOrder owl:AllDifferent \
	 --subjectOrder owl:Axiom \
	 $^ $@

# Generate SOML schema: https://github.com/VladimirAlexiev/soml/tree/master/owl2soml
# ( https://github.com/VladimirAlexiev/soml/blob/master/bin/owl2soml.pl )
cim-subset-pretty-ontology.yaml: cim-subset-pretty-ontology.ttl
	perl -S owl2soml.pl -id cim -label CIM -name identifiedObject.name -super 1 -string 2 $^ > $@

