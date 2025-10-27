from ..searching import *

_combined_cycle = contains("name", "combined cycle")
_electricity = contains("name", "electricity")
_heat_and_power = contains("name", "heat and power")
_kwh = equals("unit", "kilowatt hour")
_nuclear = contains("name", "nuclear")
_oil = contains("name", " oil")
_wood_biomass = either(contains("name", " wood"), contains("name", "bio"))
_coal = either(contains("name", "hard coal"), contains("name", "lignite"))
_ng = contains("name", "natural gas")

coal_electricity = [_coal, _electricity, _kwh]

coal_chp_electricity = [_coal, _heat_and_power, _kwh]

gas_open_cycle_electricity = [_ng, _electricity, _kwh, _combined_cycle]

gas_combined_cycle_electricity = [
    contains("name", "electricity production, natural gas, combined cycle power plant"),
    _electricity,
    _kwh,
]

gas_chp_electricity = [_ng, _heat_and_power, _kwh]

oil_open_cycle_electricity = [_oil, _electricity, _kwh, exclude(_combined_cycle)]

oil_combined_cycle_electricity = [_oil, _kwh, _electricity, _combined_cycle]

oil_chp_electricity = [_oil, _heat_and_power, _kwh]

biomass_electricity = [_wood_biomass, _electricity, _kwh]

biomass_chp_electricity = [_wood_biomass, _heat_and_power, _kwh, _combined_cycle]

biomass_combined_cycle_electricity = [
    _wood_biomass,
    _electricity,
    _kwh,
    _combined_cycle,
]

nuclear_electricity = [_nuclear, _electricity, _kwh]
