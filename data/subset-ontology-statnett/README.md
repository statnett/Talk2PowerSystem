# Ontology Subsets from Statnett Production Data

Task: https://github.com/statnett/Talk2PowerSystem_PM/issues/202

## Input and Problems

The subsets are exportd from three CIM verisons in use at Statnett, each sampled from a different model:
- `ontology_ems_cim15.ttl`
- `ontology_sa_cim16.ttl`
- `ontology_kam_cim17.ttl`

Two of the exports have FORM annotatations (translations, idmapping statistics, etc)
that can be safely ignored (TODO should we omit from query?):
- `form_ann:idmap_mapped, form_ann:idmap_total`
- TODO more

Problems:
- To fetch enum values, [ontology-query.rq](https://github.com/statnett/Talk2PowerSystem/blob/main/data/subset-ontology/ontology-query.rq) looks for `?thing a cim:IdentifiedObject; ?prop ?x`.
  However, the prefix `cim:` needs to be adjusted to the actual prefix used in the data
  - For example, no value `entsoe:AsynchronousMachineType.*` is present in `ems`
  - DONE: fixed in query
- The query doesn't look to fetch `oneOf` members (that's and older representation), so
```ttl
owl:oneOf _:genid-32525b7bc155485894a969f5cc9face72394221-AsynchronousMachineType2emotor .
```
Becomes this empty blank node:
```ttl
entsoe:AsynchronousMachineType owl:oneOf  [].
```
But that's ok since there should be the opposite link: `<value> rdf:type <enumClass>`

## Ontology Observations
- The 3 files use older namespaces: `cim15, cim16, cim17, eu1, nc1, uml1`
- They also use extra namespaces `alstom, cdpsm, entsoe_prof, entsoe_sch, eu_ext, form, form_ann, iso61968, nek, pti, statnett`:
```ttl
@prefix alstom:      <http://www.alstom.com/grid/CIM-schema-cim15-extension#> .
@prefix cdpsm:       <http://iec.ch/TC57/CIM/CDPSM/SchemaExtension/2/0#> .
@prefix cim15:       <http://iec.ch/TC57/2010/CIM-schema-cim15#> .
@prefix cim16:       <http://iec.ch/TC57/2013/CIM-schema-cim16#>.
@prefix cim17:       <http://iec.ch/TC57/CIM100#> .
@prefix entsoe_prof: <http://entsoe.eu/Secretariat/ProfileExtension/1#> .
@prefix entsoe_sch:  <http://entsoe.eu/CIM/SchemaExtension/3/1#> .
@prefix eu1:         <http://iec.ch/TC57/CIM100-EuropeanExtension/1/0#> .
@prefix eu_ext:      <http://iec.ch/TC57/CIM100-EuropeanExtension/1/0#> .
@prefix form:        <https://form.statnett.no/voc/form-ksd-extensions#> .
@prefix form_ann:    <https://form.statnett.no/schema/annotation#> .
@prefix iec61968:    <http://iec.ch/TC57/Inf/61968#> .
@prefix nc1:         <http://entsoe.eu/ns/nc#>.
@prefix nek:         <http://NEK.no/NK57/CIM/CIM100-Extension/1/0#>.
@prefix pti:         <http://www.pti-us.com/PTI_CIM-schema-cim16#> .
@prefix statnett:    <http://www.statnett.no/CIM-schema-cim15-extension#> .
@prefix uml1:        <http://langdale.com.au/2005/UML#> .
```
- I add these prefixes (to prefixes.ttl) and prepend them when prettifying (see `Makefile`).
- Then I check for missed prefixes like this:
```
grep "<ht" *_pretty*|grep -v "@prefix"
```

- Unicode problems in description of `UnitSymbol` etc:
> The degree symbol \"�\" is replaced with the letters \"deg\"

Causes these warnings:
```
cat prefixes.ttl ontology_kam_cim17.ttl > temp.ttl
owl.bat write --useCommaByDefault temp.ttl ontology_kam_cim17_pretty.ttl
WARN o.a.j.riot: [line: 3174, col: 722] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 3174, col: 836] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 3185, col: 1185] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 3742, col: 160] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 3742, col: 169] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 3742, col: 218] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 3742, col: 224] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 4812, col: 312] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 4812, col: 317] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 7589, col: 142] Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 7691, col: 322] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 7691, col: 344] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 7743, col: 11] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 7743, col: 13] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 7743, col: 75] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 7743, col: 81] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 8490, col: 722] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 8490, col: 836] Input has Unicode replacement character U+FFFD in string
WARN o.a.j.riot: [line: 8509, col: 1185] Input has Unicode replacement character U+FFFD in string
```
- Some line breaks in descriptions are written as `\r` instead of `\n`
- `kam` uses multiple inheritance, which no other CIM ontology uses.
```ttl
cim17:ACLineSegment  rdfs:subClassOf nek:NEKACLineSegment, cim17:Conductor ;
```
These have no superclasses and are like "traits" that serve to hold a number of extra props.
Added as a use-case in [Inst4CIM-KG#172](https://github.com/Sveino/Inst4CIM-KG/issues/172) CIM needs traits/mixins/flavors; and/or multiple hierarchy/typing:
```ttl
nek:NEKACLineSegment a owl:Class ; rdfs:comment "A NEK extension class" .
nek:NEKACLineSegmentPhase a owl:Class ; rdfs:comment "A NEK extension class" .
```
- Includes EA metadata. DONE ignored in query. Examples:
```ttl
uml:id "_E31A9764-F65A-4a70-B936-6128A32C0353".
form:Substation.isConnectedToRegionalGrid uml:id "_CONNECTED_TO_REGIONAL_GRID_ID" .
```
- Includes some `@no` labels and descriptions, eg
```ttl
cim17:Bay rdfs:label "Bay", "Felt"@nb ;
```
- `sa` has wrong multvalued cardinality annotation:
```ttl
entsoe_sch:IdentifiedObject.shortName cims:multiplicity cims:M:0..1, cims:M:1..1 ;
```
- `sa` spells `cims:M:1` variously as `cims:M:1..1`, which causes multiple values for at least this term:
```ttl
cim16:TopologicalNode.BaseVoltage cims:multiplicity cims:M:1, cims:M:1..1
```
- Instead of standard `inverseOf`, uses
  `cims:inverseRoleName` with annotation `owl:sameAs owl:inverseOf`
- Cardinality is expressed in a variety of ways:
  - `sa` uses `cims:multiplicity` that is a custom prop and expresses the cardinality precisely
  - `ems, kam` use `owl:FunctionalProperty, InverseFunctionalProperty` 
    that are standard but only express single-valuedness in the forward/inverse direction
    (don't express requiredness, nor a precise upper bound)
  - The best practice is to use both ways of expressing cardinality
- Neither treats datatype props and quantity kinds in a proper way:
  - `ems` and `ka` declare DatatypeProperties to have range that's not a datatype:
```ttl
# ems
cim15:StaticVarCompensator.inductiveRating a owl:DatatypeProperty, owl:FunctionalProperty, rdf:Property ;
  rdfs:range cim15:Reactance ;

# ka
cim17:ACLineSegment.b0ch a owl:DatatypeProperty, owl:FunctionalProperty, rdf:Property ;
  rdfs:range cim17:Susceptance ;
```
  - `sa` doesn't declare props as DatatypeProperty 
     and uses `cims:dataType` instead of `rdfs:range` and XSD datatypes:
```ttl
cim16:ACDCConverter.numberOfValves a rdf:Property ;
  rdfs:label "numberOfValves"@en ;
  cims:dataType cim16:Integer ;
```
