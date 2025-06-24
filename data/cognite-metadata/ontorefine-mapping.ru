PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
BASE <http://example.com/>
PREFIX cim:     <https://cim.ucaiug.io/ns#>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX unit: <http://qudt.org/vocab/unit/>

CONSTRUCT {
	?MRID a cim:Analog ;
      cim:Measurement.isInCognite true;
   	  cim:Measurement.PowerSystemResource ?PowerSystemResource ;
      cim:IdentifiedObject.mRID ?c_mrid	;
      cim:IdentifiedObject.name ?name ;
      cim:IdentifiedObject.description ?description ;
      cim:Measurement.PowerSystemResource ?PowerSystemResource ;
      cim:Analog.positiveFlowIn ?positiveFlowIn ;
      cim:Measurement.measurementType ?metadata_measurementType ;
      cim:Measurement.unitSymbol ?metadata_unit_symbol ;
      cim:Measurement.unitMultiplier ?metadata_unit_multiplier ;
      qudt:hasUnit ?qudt_hasUnit ;
    .
}
WHERE {
  BIND( ?c_external_id AS ?external_id ) .
  BIND( uri(concat("urn:uuid:",?c_mrid)) AS ?MRID ) .
  BIND( ?c_name AS ?name ) .
  BIND( ?c_is_string AS ?is_string ) .
  BIND( ?c_unit AS ?unit ) .
  BIND( ?c_unitMultiplier AS ?unitMultiplier ) .
  BIND( uri(concat(str(unit:),?c_qudt_hasUnit)) AS ?qudt_hasUnit ) .
  BIND( ?c_asset_id AS ?asset_id ) .
  BIND( ?c_is_step AS ?is_step ) .
  BIND( ?c_description AS ?description ) .
  BIND( ?c_data_set_id AS ?data_set_id ) .
  BIND( ?c_id AS ?id ) .
  BIND( ?c_created_time AS ?created_time ) .
  BIND( ?c_last_updated_time AS ?last_updated_time ) .
  BIND( ?c_metadata_measurementType AS ?metadata_measurementType ) .
  BIND( ?c_metadata_timeseriesType AS ?metadata_timeseriesType ) .
  BIND( ?c_metadata_table AS ?metadata_table ) .
  BIND( ?c_metadata_PRIS_VALUTA AS ?metadata_PRIS_VALUTA ) .
  BIND( ?c_metadata_PRIS_TYPE AS ?metadata_PRIS_TYPE ) .
  BIND( ?c_metadata_PRIS_OMRAADE_TYPE AS ?metadata_PRIS_OMRAADE_TYPE ) .
  BIND( ?c_metadata_PRIS_OMRAADE AS ?metadata_PRIS_OMRAADE ) .
  BIND( uri(?c_PowerSystemResource) AS ?PowerSystemResource ) .
  BIND( ?c_metadata_source AS ?metadata_source ) .
  BIND( ?c_metadata_topic AS ?metadata_topic ) .
  BIND( ?c_metadata_measurement_type AS ?metadata_measurement_type ) .
  BIND( ?c_metadata_timeseries_type AS ?metadata_timeseries_type ) .
  BIND( uri(concat(str(cim:),"UnitMultiplier.",?c_metadata_unit_multiplier)) AS ?metadata_unit_multiplier ) .
  BIND( uri(concat(str(cim:),"UnitSymbol.",?c_metadata_unit_symbol)) AS ?metadata_unit_symbol ) .
  BIND( ?c_metadata_mrid AS ?metadata_mrid ) .
  BIND( ?c_metadata_unit AS ?metadata_unit ) .
  BIND( ?c_metadata_substation AS ?metadata_substation ) .
  BIND( ?c_metadata_end_time AS ?metadata_end_time ) .
  BIND( ?c_metadata_subscription AS ?metadata_subscription ) .
  BIND( ?c_metadata_device AS ?metadata_device ) .
  BIND( ?c_metadata_kafka_stream AS ?metadata_kafka_stream ) .
  BIND( xsd:boolean(?c_positiveFlowIn) as ?positiveFlowIn)
 }