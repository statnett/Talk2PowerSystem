PREFIX cim:          <https://cim.ucaiug.io/ns#>
PREFIX autocomplete: <http://www.ontotext.com/plugins/autocomplete#>
PREFIX rdfs:         <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
    cim:IdentifiedObject.name      autocomplete:addLabelConfig "" .
    cim:CoordinateSystem.crsUrn    autocomplete:addLabelConfig "" .
    cim:IdentifiedObject.aliasName autocomplete:addLabelConfig "" .
    rdfs:label                     autocomplete:removeLabelConfig "" .
    [] autocomplete:enabled true .
}
