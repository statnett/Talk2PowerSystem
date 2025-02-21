See [Demo1](https://github.com/statnett/Talk2PowerSystem/wiki/Demo1) in the wiki for a description.

- [templates.yaml](./templates.yaml) - the competency questions templates, created manually by humans
- [CQAGC-Candidates-10_Answers--1.json](./CQAGC-Candidates-10_Answers--1.json) - gold standard corpus of questions, automatically generated from the templates, where we sample up to 10 questions from each template
- [nordic44-ontology-query.rq](./nordic44-ontology-query.rq) - the SPARQL query to collect the ontology schema
- [nordic44-ontology.ttl](./nordic44-ontology.ttl) - the collected ontology schema in turtle format
- [nordic44.config](./nordic44.config) - the LLM configuration
- [eval_summary.json](./eval_summary.json) - summary of the evaluation results
- [eval_results.json](./eval_results.json) - detailed results per question
- [eval.log](eval.log) - detailed log from the evaluation
