This is a demo of NLQ over 5 competency questions, before the project kickoff (2025-02-20).
- TODO link to wiki
- TODO list issues

`templates.yaml` contains 4 out of the 5 competency questions templates.
From these templates we automatically generate a gold standard corpus `CQAGC-Candidates-10_Answers--1.yaml`,
where we sample up to 10 questions from each template.

`nordic44-ontology-query.rq` is the SPARQL query to collect the ontology schema.
The results of the execution are in the file `nordic44.ttl`.

`nordic44.config` contains the LLM configuration.

The evaluation results are attached in the two json files.
