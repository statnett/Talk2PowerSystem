#!/usr/bin/env python3

import argparse
import os
import requests
import tempfile
import shutil
import json
import gzip
import time
from pathlib import Path
from typing import Optional

def get_credentials_from_env() -> tuple[Optional[str], Optional[str]]:
    """Get credentials from environment variables."""
    username = os.environ.get('CIMUSER')
    password = os.environ.get('CIMPASSWORD')
    return username, password

class GraphDBLoader:
    def __init__(
        self,
        graphdb_url: str = "http://localhost:7200",
        repository_name: str = "cim",
        config_file: str = "resources/repo-config.ttl",
        ontology_graph: str = "https://cim.ucaiug.io/ns#graph",
        ontologies_list: str = "ontologies.txt",
        instances_list: str = "instances.txt",
        username: Optional[str] = None,
        password: Optional[str] = None,
        force: bool = False,
        no_auth: bool = False
    ):
        self.graphdb_url = graphdb_url
        self.repository_name = repository_name
        self.config_file = config_file
        self.ontology_graph = ontology_graph
        self.ontologies_list = ontologies_list
        self.instances_list = instances_list
        self.force = force
        
        # Get credentials from args or environment variables
        if not no_auth:
            if username is None or password is None:
                env_username, env_password = get_credentials_from_env()
                username = username or env_username
                password = password or env_password
                
            self.auth = (username, password) if username and password else None
        else:
            self.auth = None
            
        self.temp_dir = Path(tempfile.mkdtemp())

    def file_chunker(self,file_obj, chunk_size=1024 * 256):  # 1 MB default chunks
        while True:
            data = file_obj.read(chunk_size)
            if not data:
                break
            yield data

    def print_response(self, response: requests.Response, operation: str):
        """Print response details from GraphDB REST API."""
        print(f"\n=== {operation} Response ===")
        print(f"Status Code: {response.status_code}")
        print("Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # Try to parse and print response content if it exists
        if response.content:
            try:
                # Try to parse as JSON
                content = response.json()
                print("Response Content (JSON):")
                print(json.dumps(content, indent=2))
            except json.JSONDecodeError:
                # If not JSON, print as text
                print("Response Content (Text):")
                print(response.text)
        print("========================\n")

    def execute_sparql_query(self, query_file: str) -> bool:
        """Execute a SPARQL query from a .ru file."""
        print(f"Executing SPARQL query from {query_file}...")
        
        with open(query_file, 'r') as f:
            query = f.read()

        response = requests.post(
            f"{self.graphdb_url}/repositories/{self.repository_name}/statements",
            data={'update': query},
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            auth=self.auth
        )

        self.print_response(response, f"Execute SPARQL Query: {os.path.basename(query_file)}")

        if response.status_code in [200, 204]:
            print(f"Successfully executed query from {query_file}")
            return True
        else:
            print(f"Error: Failed to execute query from {query_file}. Status code: {response.status_code}")
            return False

    def execute_all_queries(self):
        """Execute all .ru files in the resources/queries directory."""
        query_dir = Path("resources/queries")
        if not query_dir.exists():
            print(f"Warning: Query directory {query_dir} does not exist")
            return

        print("\nExecuting SPARQL queries...")
        query_files = list(query_dir.glob("*.ru"))
        
        if not query_files:
            print("No .ru files found in resources/queries directory")
            return

        for query_file in query_files:
            if not self.execute_sparql_query(str(query_file)):
                raise Exception(f"Failed to execute query: {query_file}")

    def validate_files(self):
        """Validate that all required files exist."""
        required_files = [
            self.config_file,
            self.ontologies_list,
            self.instances_list
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Required file '{file_path}' does not exist")

    def create_repository(self) -> bool:
        """Create the GraphDB repository using the configuration file."""
        print(f"Creating repository using configuration from '{self.config_file}'...")
        
        with open(self.config_file, 'rb') as f:
            files = {'config': f}
            response = requests.post(
                f"{self.graphdb_url}/rest/repositories",
                files=files,
                auth=self.auth
            )
        
        self.print_response(response, "Create Repository")
        
        if response.status_code == 201:
            print("Repository created successfully")
            return True
        else:
            print(f"Error: Failed to create repository. Status code: {response.status_code}")
            return False

    def load_ontology(self, ontology_url: str) -> bool:
        """Load a single ontology file into GraphDB."""
        filename = os.path.basename(ontology_url)
        local_file = self.temp_dir / filename

        print(f"Downloading {ontology_url}...")
        response = requests.get(ontology_url)
        if response.status_code != 200:
            print(f"Error: Failed to download {ontology_url}")
            return False

        with open(local_file, 'wb') as f:
            f.write(response.content)

        print(f"Loading {filename} into named graph '{self.ontology_graph}'...")
        with open(local_file, 'rb') as f:
            compressed_data = gzip.compress(f.read())
            response = requests.post(
                f"{self.graphdb_url}/repositories/{self.repository_name}/rdf-graphs/service",
                params={'graph': self.ontology_graph},
                data=compressed_data,
                headers={'Content-Type': 'application/x-turtle','Content-Encoding': 'gzip'},
                auth=self.auth
            )

        self.print_response(response, f"Load Ontology: {filename}")

        if response.status_code == 204:
            print(f"Successfully loaded {filename}")
            return True
        else:
            print(f"Error: Failed to load {filename}. Status code: {response.status_code}")
            return False

    def load_instance(self, instance_url: str) -> bool:
        """Load a single instance file into GraphDB."""
        filename = os.path.basename(instance_url)
        local_file = self.temp_dir / filename

        print(f"Downloading {instance_url}...")
        response = requests.get(instance_url)
        if response.status_code != 200:
            print(f"Error: Failed to download {instance_url}")
            return False

        with open(local_file, 'wb') as f:
            f.write(response.content)

        print(f"Loading {filename}...")
        with open(local_file, 'rb') as f:
            compressed_data = gzip.compress(f.read())
            response = requests.post(
                f"{self.graphdb_url}/repositories/{self.repository_name}/statements",
                data=compressed_data,
                headers={'Content-Type': 'application/trig', 'Content-Encoding': 'gzip'},
                auth=self.auth
            )

        self.print_response(response, f"Load Instance: {filename}")

        if response.status_code == 204:
            print(f"Successfully loaded {filename}")
            return True
        else:
            print(f"Error: Failed to load {filename}. Status code: {response.status_code}")
            return False

    def update_autocomplete_labels(self, labels_file: str = "autocomplete-labels.txt"):
        """Update autocomplete labels from a file."""
        print(f"Updating autocomplete labels from {labels_file}...")

        response = requests.delete(
            f"{self.graphdb_url}/rest/autocomplete/labels",
            json={"labelIri":"http://www.w3.org/2000/01/rdf-schema#label","languages":""},
            headers={"x-graphdb-repository": self.repository_name},
            auth=self.auth
        )

        if not os.path.exists(labels_file):
            print(f"Warning: Labels file '{labels_file}' not found.")
            return

        with open(labels_file, 'r') as f:
            for line in f:
                label_iri = line.strip()
                if not label_iri:
                    continue

                payload = {
                    "labelIri": label_iri,
                    "languages": ""
                }

                response = requests.put(
                    f"{self.graphdb_url}/rest/autocomplete/labels",
                    json=payload,
                    headers={"x-graphdb-repository": self.repository_name},
                    auth=self.auth
                )

                self.print_response(response, f"Update Autocomplete Label: {label_iri}")

                if response.status_code not in [200, 204, 201]:
                    print(f"Error: Failed to update autocomplete label '{label_iri}'. Status code: {response.status_code}")
        
        response = requests.post(
            f"{self.graphdb_url}/rest/autocomplete/enabled?enabled=true",
            headers={"x-graphdb-repository": self.repository_name},
            auth=self.auth
        )

        response = requests.post(
            f"{self.graphdb_url}/rest/autocomplete/reindex",
            headers={"x-graphdb-repository": self.repository_name},
            auth=self.auth
        )
        
        response = requests.post(
            f"{self.graphdb_url}/rest/rdfrank/compute",
            headers={"x-graphdb-repository": self.repository_name},
            auth=self.auth
        )

    def process_files(self):
        """Process all ontology and instance files."""
        # Load ontologies
        print("Loading ontology files...")
        with open(self.ontologies_list, 'r') as f:
            for line in f:
                ontology_url = line.strip()
                if ontology_url and not self.load_ontology(ontology_url):
                    raise Exception(f"Failed to load ontology: {ontology_url}")

        # Load instances
        print("Loading instance files...")
        with open(self.instances_list, 'r') as f:
            for line in f:
                instance_url = line.strip()
                if instance_url and not self.load_instance(instance_url):
                    raise Exception(f"Failed to load instance: {instance_url}")

    def cleanup(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)

    def delete_repository(self) -> bool:
        """Delete the repository if it exists."""
        print(f"Checking if repository '{self.repository_name}' exists...")
        
        # First check if repository exists
        response = requests.get(
            f"{self.graphdb_url}/rest/repositories/{self.repository_name}",
            auth=self.auth
        )
        
        if response.status_code == 404:
            print(f"Repository '{self.repository_name}' does not exist")
            return True
            
        if response.status_code != 200:
            print(f"Error checking repository existence. Status code: {response.status_code}")
            return False
            
        print(f"Deleting repository '{self.repository_name}'...")
        response = requests.delete(
            f"{self.graphdb_url}/rest/repositories/{self.repository_name}",
            auth=self.auth
        )
        
        self.print_response(response, "Delete Repository")
        
        if response.status_code == 200:
            print(f"Successfully deleted repository '{self.repository_name}'")
            print("Waiting 5 seconds for GraphDB to process the deletion...")
            time.sleep(5)
            return True
        else:
            print(f"Error: Failed to delete repository. Status code: {response.status_code}")
            return False

    def run(self):
        """Run the complete loading process."""
        try:
            self.validate_files()
            
            # Delete repository if force option is enabled
            if self.force:
                if not self.delete_repository():
                    raise Exception("Failed to delete existing repository")
            
            if self.create_repository():
                self.process_files()
                self.execute_all_queries()
                self.update_autocomplete_labels()
        finally:
            self.cleanup()

def main():
    parser = argparse.ArgumentParser(description='Load ontologies and instances into GraphDB')
    parser.add_argument('-u', '--url', default='http://localhost:7200',
                      help='GraphDB server URL')
    parser.add_argument('-r', '--repository', default='cim',
                      help='Repository name')
    parser.add_argument('-c', '--config', default='resources/repo-config.ttl',
                      help='Repository configuration file')
    parser.add_argument('-g', '--graph', default='https://cim.ucaiug.io/ns#graph',
                      help='Named graph URI')
    parser.add_argument('-l', '--list', default='ontologies.txt',
                      help='List of ontology files')
    parser.add_argument('-i', '--instances', default='instances.txt',
                      help='List of instance files')
    parser.add_argument('-U', '--username',
                      help='Username for authentication (overrides CIMUSER env var)')
    parser.add_argument('-P', '--password',
                      help='Password for authentication (overrides CIMPASSWORD env var)')
    parser.add_argument('--force', action='store_true',
                      help='Force recreation of repository by deleting it if it exists')
    parser.add_argument('--no-auth', action='store_true',
                      help='Force execution without authentication, even if credentials are available')

    args = parser.parse_args()

    loader = GraphDBLoader(
        graphdb_url=args.url,
        repository_name=args.repository,
        config_file=args.config,
        ontology_graph=args.graph,
        ontologies_list=args.list,
        instances_list=args.instances,
        username=args.username,
        password=args.password,
        force=args.force,
        no_auth=args.no_auth
    )

    loader.run()

if __name__ == '__main__':
    main() 