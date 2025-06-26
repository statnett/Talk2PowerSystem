# RDF-ization of cognite metadata

Tasks: [#105](https://github.com/statnett/Talk2PowerSystem_PM/issues/105) and
[#112](https://github.com/statnett/Talk2PowerSystem_PM/issues/112)

Added to graph [cim:Measurement.isInCognite.graph](https://cim.ontotext.com/graphdb/resource?uri=https:%2F%2Fcim.ucaiug.io%2Fns%23Measurement.isInCognite.graph&role=context)

# Example data 

There are 3 kinds of records:
Price, Flow and Exchange Rate

## Price

```json
    {
        "external_id": "Kraftpriser_NO3_NOK_13",
        "name": "Kraftpriser_NO3_NOK",
        "is_string": false,
        "metadata": {
            "PRIS_TYPE": "PRI7004",
            "measurementType": "Price",
            "PRIS_OMRAADE_TYPE": "1.0",
            "PRIS_OMRAADE": "NO3",
            "timeseriesType": "value",
            "table": "MMS.RAPPORT_KRAFTPRIS_ELSPOT_NO",
            "PRIS_VALUTA": "NOK"
        },
        "unit": "NOK per MWh",
        "asset_id": 2149735182077095,
        "is_step": false,
        "description": "Kraftpriser for prisomrade NO3 (NOK)",
        "security_categories": [],
        "data_set_id": 7519740957219860,
        "id": 2896958021852,
        "created_time": "2020-05-05 20:11:02.889+00:00",
        "last_updated_time": "2024-12-02 15:41:40.072+00:00"
    },
```
We propose to map it to something like this (TODO: existence of props is not checked!):

```ttl
<urn:uuid:new-mRID> a cim:Analog;
  cim:Measurement.isInCognite true;
  cim:IdentifiedObject.mRID "new-mRID";
  cim:IdentifiedObject.name "Kraftpriser_NO3_NOK_13";
  cim:IdentifiedObject.description "Kraftpriser for prisomrade NO3 (NOK)";
  cim:Measurement.PowerSystemResource <urn:uuid:mRID-of-NO3>; # manual lookup
  cim:Measurement.measurementType "Price-Actual";
  cim:Measurement.unitSymbol cim:UnitSymbol.NOKperMWh ;
  qudt:hasUnit unit:CCY_NOK-PER-MegaW-HR.
```

Notes:
- a new mRID is generated. @olavalstad needs to add it as second value of `external_id` in Cognite (we'll give a mapping table)
- https://github.com/Sveino/Inst4CIM-KG/issues/168 for `cim:UnitSymbol.NOKperMWh`, which doesn't exist in CIM
- ignored fields: `PRIS_TYPE, PRIS_OMRAADE_TYPE, table, is_string, is_step, created_time, last_updated_time`
    - `timeseriesType`: "value" means Actual, which we've mixed into `measurementType`
    - `name` because the longer `external_id` is used
    - `PRIS_VALUTA` because `unit` is used
    - `id, asset_id, data_set_id` because these are internal Cognite ids

## Flow

```json
   {
        "external_id": "292350c3-1edf-8b57-e050-1e828c94898c_estimated_value",
        "name": "Elspot NO3-NO5 MW_estimated_value",
        "is_string": false,
        "metadata": {
            "source": "eTerra",
            "topic": "observations_grid_power_no_ems_analog_active_power_res_1s_avro_v1",
            "measurement_type": "ThreePhaseActivePower",
            "timeseries_type": "estimated_value",
            "unit_multiplier": "M",
            "unit_symbol": "W",
            "mrid": "292350c3-1edf-8b57-e050-1e828c94898c",
            "unit": "MW",
            "substation": "DIV_NCC",
            "end_time": "",
            "subscription": "DIV_NCC",
            "device": "ELSPOT"
        },
        "unit": "MW",
        "asset_id": 2501745549637880,
        "is_step": false,
        "description": "ThreePhaseActivePower",
        "security_categories": [],
        "data_set_id": 5515145765342807,
        "id": 5968936028135778,
        "created_time": "2023-06-16 00:06:04.901+00:00",
        "last_updated_time": "2025-01-06 14:33:18.557+00:00"
    },
```
We propose to map it to:

```ttl
<urn:uuid:9bb00faf-0f2f-831a-e040-1e828c94e833> a cim:Analog;
  cim:Measurement.isInCognite true;
  cim:IdentifiedObject.mRID "9bb00faf-0f2f-831a-e040-1e828c94e833";
  cim:IdentifiedObject.name "Elspot NO3-NO5 MW_estimated_value";
  cim:IdentifiedObject.description "topic: observations_grid_power_no_ems_analog_active_power_res_1s_avro_v1";
  cim:Measurement.PowerSystemResource  <urn:uuid:mRID-of-NO3-NO5-BiddingZoneBorder>; # manual lookup
  cim:Analog.positiveFlowIn true; # because the border is defined NO3-NO5. For the opposite, should be false
  cim:Measurement.measurementType "ThreePhaseActivePower-Flow-Estimated";
  cim:Measurement.unitMultiplier cim:UnitSymbol.M;
  cim:Measurement.unitSymbol cim:UnitSymbol.W;
  qudt:hasUnit qudt:MegaW.
```
Notes:
- @olavalstad needs to add the pure mRID as second value of `external_id` in Cognite (we'll give a mapping table)
- We add a second `Measurement.PowerSystemResource2` to express the target zone.
  Such doesn't exist in the CIM, so we need to add its definition to `cimr.ttl (new name of `cimex.ttl`) but will use the `cim:` namespace: (cc @Sveino)
  https://github.com/Sveino/Inst4CIM-KG/issues/169
- We add some structure to `measurementType` as a 3-part string, but there are better ways:
  https://github.com/Sveino/Inst4CIM-KG/issues/170
- We ignore some Cognite fields, as explained above
    - in addition, we ignore `"substation": "DIV_NCC"`: since I don't understand it: I googled for `DIV_NCC` and came up empty (@Sveino)

## Exchange Rate

```json
    {
        "external_id": "Valutakurs_EUR_NOK",
        "name": "Valutakurs_EUR_NOK",
        "is_string": false,
        "metadata": {
            "kafka_stream": "connect_ogg_fifty_MMS_RAPPORT_KRAFTPRIS_ELSPOT_NO_avro",
            "ENDRET_AV": "Fifty",
            "measurementType": "Price",
            "BASIS_VALUTA": "EUR",
            "timeseriesType": "value",
            "table": "MMS.VALUTA_KURS",
            "PRIS_VALUTA": "NOK"
        },
        "unit": "[NOK/EUR]",
        "asset_id": 8047786047018709,
        "is_step": false,
        "description": "Valutakurs for EUR NOK",
        "security_categories": [],
        "data_set_id": 7519740957219860,
        "id": 6435797444291554,
        "created_time": "2019-11-25 08:23:38.904+00:00",
        "last_updated_time": "2024-11-27 15:57:27.349+00:00"
    },
```
We propose to map it to something like this:

```ttl
<urn:uuid:new-mRID> a cim:Analog;
  cim:Measurement.isInCognite true;
  cim:IdentifiedObject.mRID "new-mRID";
  cim:IdentifiedObject.name "Valutakurs_EUR_NOK";
  cim:IdentifiedObject.description "Valutakurs for EUR NOK. kafka_stream: connect_ogg_fifty_MMS_RAPPORT_KRAFTPRIS_ELSPOT_NO_avro";
  cim:Measurement.measurementType "CurrencyExchange-Actual";
  cim:Measurement.unitSymbol cim:UnitSymbol.NOKperEUR.
```

Notes:
- a new mRID is generated. @olavalstad needs to add it as second value of `external_id` in Cognite (we'll give a mapping table)
- https://github.com/Sveino/Inst4CIM-KG/issues/168 for `cim:UnitSymbol.NOKperEUR`, which doesn't exist in CIM
- ignored fields: `ENDRET_AV, table, is_string, is_step, created_time, last_updated_time`
    - `"measurementType": "Price"` is wrong because an exchange rate is not really a price
    - `timeseriesType`: "value" means Actual, which we've mixed into `measurementType`
    - `PRIS_VALUTA` is rolled into unitSymbol
    - `id, asset_id, data_set_id` because these are internal Cognite ids

# JSON remarks

* exists both `metadata.measuerment_type` and `metadata.measurementType`
 
# CIM remarks

ordering consistantly the elements in the labels of `nc:BiddingZoneBorder` will make for easier reconciliation 
`NO5 - NO1` --> `NO1 - NO5`

```spaqrl
PREFIX cim: <https://cim.ucaiug.io/ns#>
PREFIX nc: <https://cim4.eu/ns/nc#>
select * where {
    ?x a nc:BiddingZoneBorder ; cim:IdentifiedObject.name ?name 
} limit 100
```