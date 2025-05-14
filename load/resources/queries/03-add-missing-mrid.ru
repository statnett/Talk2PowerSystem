PREFIX cimex: <https://rawgit2.com/statnett/Talk2PowerSystem/main/demo1/cimex/>
PREFIX cim: <https://cim.ucaiug.io/ns#>
insert {
    graph cimex:mridSignificantPart {
    	?x cim:IdentifiedObject.mRID ?id.
    }
} where {
  ?x a cim:IdentifiedObject
  bind (strafter(str(?x),"#_") as ?id)
  filter not exists {?x cim:IdentifiedObject.mRID [] }
}