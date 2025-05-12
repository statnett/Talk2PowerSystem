# Loader script for Nordic44

- Creates a repository from [nordic44-repo-config.ttl](resources/nordic44-repo-config.ttl)
- Loads [cimex.ttl](resources/cimex.ttl) in a named graph `https://cim.ucaiug.io/ns#graph`
- Loads all files from [ontologies.txt] in `https://cim.ucaiug.io/ns#graph`
- Loads all instance data from [instances.txt] in the graph specified in the file
- Loads custom inference rules from [cim_owl2-rl-optimized.pie](resources/cim_owl2-rl-optimized.pie)

https://graphdb.ontotext.com/documentation/11.0/configuring-a-repository.html

- ttl repository configuration
- enable autocomplete
    - see https://graphwise.atlassian.net/browse/GDB-12211
- load custom inference using spaqrl
    - see https://github.com/statnett/Talk2PowerSystem/wiki/Inference
- load ontologies
  - https://github.com/Sveino/Inst4CIM-KG/tree/develop/rdfs-improved: CGMES/ttl and CGMES-NC/ttl
  - in graph <https://cim.ucaiug.io/ns#graph>
- load trig data fom github locations
    - https://github.com/statnett/Nordic44/tree/main/instances/Enterprise/trig
- visual graphs

[Enterprise](../Nordic44/instances/Enterprise)
[Grid](../Nordic44/instances/Grid)
[NetworkCode](../Nordic44/instances/NetworkCode)
