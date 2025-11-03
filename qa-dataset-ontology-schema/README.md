# Q&A Dataset Ontology Schema

The N-Shot Tool finds top-N questions from the Q&A dataset that are most similar to the user's question,
and serves them together with the associated SPARQL templates to the chatbot as N-shot examples.

We use [ChatGPT Retrieval GraphDB Connector](https://graphdb.ontotext.com/documentation/11.1/retrieval-graphdb-connector.html) to index database entities to a vector database and then retrieve them quickly.
This module holds the needed artefacts:
- A simple ontology definition for storing the Q&A dataset in GraphDB
- ChatGPT Retrieval Connector definition
- GraphDB repository configuration
