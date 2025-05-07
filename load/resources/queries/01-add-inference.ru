PREFIX sys: <http://www.ontotext.com/owlim/system#>
INSERT DATA {
    <_:cim-owl-rl-optimised> sys:addRuleset <https://raw.githubusercontent.com/statnett/Talk2PowerSystem/refs/heads/main/cim_owl2-rl-optimized.pie> .
    [] sys:defaultRuleset "cim-owl-rl-optimised". 
    [] sys:reinfer [].
}