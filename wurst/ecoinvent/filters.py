from ..searching import *

coal_electricity = [
    either(contains('name', 'hard coal'), contains('name', 'lignite')),
    contains('name', 'electricity'),  # Do we need this?
    equals('unit', 'kilowatt hour'),
]

coal_chp_electricity = [
    either(contains('name', 'hard coal'), contains('name', 'lignite')),
    contains('name', 'heat and power'),
    equals('unit', 'kilowatt hour')
]

gas_open_cycle_electricity = [
    contains('name', 'natural gas'),
    contains('name', 'electricity'),
    equals('unit', 'kilowatt hour'),
    exclude(contains('name', 'combined cycle')),
]

gas_combined_cycle_electricity = [
    contains('name', 'electricity production, natural gas, combined cycle power plant'),
    contains('name', 'electricity'),
    equals('unit', 'kilowatt hour'),
]

gas_chp_electricity = [
    contains('name', 'natural gas'),
    contains('name', 'heat and power'),
    equals('unit', 'kilowatt hour'),
]

oil_open_cycle_electricity = [
    contains('name', 'oil'),
    contains('name', 'electricity'),
    equals('unit', 'kilowatt hour'),
    exclude(contains('name', 'combined cycle')),
]

oil_combined_cycle_electricity = [
    contains('name', 'oil'),
    contains('name', 'electricity'),
    equals('unit', 'kilowatt hour'),
    contains('name', 'combined cycle'),
]

oil_chp_electricity = [
    contains('name', 'oil'),
    contains('name', 'heat and power'),
    equals('unit', 'kilowatt hour'),
]

biomass_electricity = [
    either(contains('name', 'wood'), contains('name', 'bio')),
    contains('name', 'electricity'),
    equals('unit', 'kilowatt hour')
]

biomass_chp_electricity = [
    either(contains('name', 'wood'), contains('name', 'bio')),
    contains('name', 'heat and power'),
    equals('unit', 'kilowatt hour'),
    exclude(contains('name', 'combined cycle')),
]

biomass_combined_cycle_electricity = [
    either(contains('name', 'wood'), contains('name', 'bio')),
    contains('name', 'electricity'),
    contains('name', 'combined cycle'),
    equals('unit', 'kilowatt hour'),
]

nuclear_electricity = [
    contains('name', 'nuclear'),
    contains('name', 'electricity'),
    equals('unit', 'kilowatt hour')
]
