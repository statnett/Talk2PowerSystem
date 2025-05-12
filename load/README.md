# Loader script for Nordic44

- Creates a repository from [nordic44-repo-config.ttl](resources/nordic44-repo-config.ttl)
- Loads [cimex.ttl](resources/cimex.ttl) in a named graph `https://cim.ucaiug.io/ns#graph`
- Loads all files from [ontologies.txt] in `https://cim.ucaiug.io/ns#graph`
- Loads all instance data from [instances.txt] in the graph specified in the file
- Loads custom inference rules from [cim_owl2-rl-optimized.pie](resources/cim_owl2-rl-optimized.pie)

Remaining to do

- enable autocomplete
    - see https://graphwise.atlassian.net/browse/GDB-12211

- create visual graphs
