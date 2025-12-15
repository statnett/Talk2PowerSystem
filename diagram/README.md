
# Making Diagrams

See wiki pages:
- [Diagrams](https://github.com/statnett/Talk2PowerSystem/wiki/Diagrams): not yet done
  - [Electrical Diagrams](https://github.com/statnett/Talk2PowerSystem/wiki/Electrical-Diagrams): done
  - [Visual Graph](https://github.com/statnett/Talk2PowerSystem/wiki/Visual-Graph): a lot of info about doing it by hand, but not about automatization
  
# No PowSyBl Diagrams for Telemark 

- PowSyBl cannot load Telemark120: 
  [powsybl-core#3682](https://github.com/powsybl/powsybl-core/issues/3682) Unexpected CgmesContainer for containerId on Telemark120 data powsybl/powsybl-core
- We believe the reason is this problem in Telemark-120:
  [3lbits/CIM4NoUtility#414](https://github.com/3lbits/CIM4NoUtility/issues/414) duplicate statements across named graphs

Until this problem is resolved, we don't display PowSyBl Diagrams for Telemark120.
- Out of all diagrams described in `diagrams.trig` (and extract `diagrams.tsv`):
  - 116 display only Nordic44 resources
  - 80 display also Telemark120 resources, and should be discarded

The way we fixed this is rather hacky:
- We first made `diagrams.trig` and extracted `diagrams.tsv`
- Then we ran `generate_diagrams.py`, which is driven by the list `diagrams.tsv`
- In addition to `svg/*` files, it produced `diagrams.log`
- Out of this log we extracted `diagrams-error.txt` (list of 80 diagrams to be deleted)
- Then we wrote `diagrams-delete.ru` with a list of diagrams to be deleted. We used it to:
  - Produce `diagrams-fixed.trig` (and extract `diagrams-fixed.tsv`)
  - And delete those diagrams directly from GraphDB
