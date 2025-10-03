# Loader script for Nordic44

This script helps load ontologies and instance data into a GraphDB repository for the Nordic44 power system model.
Relevant task [#18](https://github.com/statnett/Talk2PowerSystem_PM/issues/18)

## Features

- Creates a repository from [repo-config.ttl](../data/repo-config.ttl)
- Downloads and loads all files from [ontologies.txt](ontologies.txt) in `https://cim.ucaiug.io/ns#graph`
- Downloads and loads all instance data from list of files in [instances.txt](instances.txt]) in the graph specified in the `.trig` files.
- Loads custom inference rules from [cim_owl2-rl-optimized.pie](../data/cim_owl2-rl-optimized.pie). (see the [wiki](https://github.com/statnett/Talk2PowerSystem/wiki/Inference) for details)
- Executes post-loading SPARQL [queries](../data/queries/) in order w.r.t the filename.
- Enables [autocomplete](https://graphdb.ontotext.com/documentation/11.1/autocomplete-index.html) for the labels specified in [autocomplete-labels.txt](autocomplete-labels.txt)

## Prerequisites

- Python 3.x
- GraphDB server running (default: http://localhost:7200)
- GraphDB credentials (can be set via environment variables or command line)

## Setup

1. Create and activate a virtual environment:
```bash
./setup_venv.sh
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Set up credentials (optional):
```bash
export CIMUSER="your_username"
export CIMPASSWORD="your_password"
```

## Usage

Basic usage:
```bash
python load.py
```

Advanced options:
```bash
python load.py --help
```

Available options:
- `-u, --url`: GraphDB server URL (default: http://localhost:7200)
- `-r, --repository`: Repository name (default: nordic44, should be aligned with contets of config file)
- `-c, --config`: Repository configuration file (default: resources/nordic44-repo-config.ttl)
- `-g, --graph`: Named graph containing ontologies (default: https://cim.ucaiug.io/ns#graph)
- `-l, --list`: List of ontology files (default: ontologies.txt)
- `-i, --instances`: List of instance files (default: instances.txt)
- `-U, --username`: Username for authentication (overrides CIMUSER env var)
- `-P, --password`: Password for authentication (overrides CIMPASSWORD env var)
- `--force`: Force recreation of repository by deleting it if it exists
- `--no-auth`: Force execution without authentication, even if credentials are available

Example with custom parameters:
```bash
python load.py --url http://graphdb:7200 --repository my_repo --force
```

Example without authentication:
```bash
python load.py --no-auth
```

## File Structure

- `ontologies.txt`: List of ontology files to load
- `instances.txt`: List of instance files to load
- `../data`: Directory containing configuration, rule files and queries
  - `repo-config.ttl`: Repository configuration
  - `cim_owl2-rl-optimized.pie`: Custom inference rules
  - `queries/`: Directory containing SPARQL update queries
    - `01-add-inference.ru`: Sets up inference rules and triggers reinference
    - `02-add-mridSignificantPart.ru`: Adds significant part annotations
    - `03-add-missing-mrid.ru`: Adds missing mRID identifiers