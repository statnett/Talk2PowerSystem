PREFIX sys: <http://www.ontotext.com/owlim/system#>
INSERT DATA {
    <_:cim> sys:addRuleset <https://raw.githubusercontent.com/statnett/Talk2PowerSystem/refs/heads/main/data/cim.pie> .
    [] sys:defaultRuleset "cim". 
    [] sys:reinfer [].
}