PREFIX cimex: <https://rawgit2.com/statnett/Talk2PowerSystem/main/demo1/cimex/>
PREFIX cim: <https://cim.ucaiug.io/ns#>
insert {
    graph cimex:mridSignificantPart {
    	?x cimex:mridSignificantPart ?part .
    }
} where {
  ?x a cim:IdentifiedObject
  bind (strafter(str(?x),"urn:uuid:") as ?id)
  bind(replace(?id,"-.*","") as ?part)
  filter(?part!="")
}