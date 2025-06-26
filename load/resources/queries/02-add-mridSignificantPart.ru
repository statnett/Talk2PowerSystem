PREFIX cimr: <https://cim.ucaiug.io/rules#>
PREFIX cim: <https://cim.ucaiug.io/ns#>
insert {
    graph cimr:mridSignificantPart\/graph {
    	?x cimr:mridSignificantPart ?part .
    }
} where {
  ?x a cim:IdentifiedObject
  bind (strafter(str(?x),"urn:uuid:") as ?id)
  bind(replace(?id,"-.*","") as ?part)
  filter(?part!="")
}