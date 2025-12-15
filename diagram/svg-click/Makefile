all:
	grep -Po 'id="(.*?)"' ../svg/PowSyBl-SLD-2substations-KRISTIANSAND-and-ARENDAL.svg > id-all.txt
	grep -Po 'id="(.*?)"' ../svg/PowSyBl-SLD-2substations-KRISTIANSAND-and-ARENDAL.svg|sort|uniq > id-all-uniq.txt
	grep -Po 'id="id[0-9a-f]{8}_45_[0-9a-f]{4}_45_[0-9a-f]{4}_45_[0-9a-f]{4}_45_[0-9a-f]{12}.*?"' ../svg/PowSyBl-SLD-2substations-KRISTIANSAND-and-ARENDAL.svg > id-uuid-all.txt
	grep -Po 'id="id[0-9a-f]{8}_45_[0-9a-f]{4}_45_[0-9a-f]{4}_45_[0-9a-f]{4}_45_[0-9a-f]{12}.*?"' ../svg/PowSyBl-SLD-2substations-KRISTIANSAND-and-ARENDAL.svg|sort|uniq > id-uuid-uniq.txt
	perl -pe 's{_45_}{-}g; s{_95_}{_}g' id-all-uniq.txt  > id-all-norm.txt
	perl -pe 's{_45_}{-}g; s{_95_}{_}g' id-uuid-uniq.txt > id-uuid-norm.txt
	perl -pe 's{id="id([^_]+)(_.*)?"}{$$1}' id-uuid-norm.txt | uniq > uuid-mrid.txt
	perl -pe 's{[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}}{UUID}g' id-all-norm.txt | sort | uniq -c > patterns.txt
	perl -pe 's{id="(.*?)"}{$$1}; s{id}{}; s{_+}{\n}g; ' id-all-norm.txt  | sort | uniq > svg-words.txt
	perl -pe 's{([0-9a-f-]{36})-\1}{$$1}; s{(ONE|fict)-}{$$1\n}' svg-words.txt | sort | uniq > svg-dedup.txt 
	wc -l *.txt
