PREFIX cimr: <https://cim.ucaiug.io/rules#>
PREFIX cim: <https://cim.ucaiug.io/ns#>
insert {
    graph cimr:mridSignificantPart {
    	?x cim:IdentifiedObject.mRID ?id.
    }
} where {
  ?x a cim:IdentifiedObject
  bind (strafter(str(?x),"urn:uuid:") as ?id)
  filter not exists {?x cim:IdentifiedObject.mRID [] }
}