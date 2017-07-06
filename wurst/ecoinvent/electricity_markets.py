from ..searching import get_many


def get_generators_in_mix(db, name="market for electricity, high voltage"):
    """Get names of inputs to electricity mixes"""
    inputs = set()
    for act in db:
        if act['name'] == name:
            for exc in act.technosphere():
                producer = exc.input
                if producer['unit'] == 'kilowatt hour':
                    inputs.add(producer['name'])
    return inputs


# Valid as of 3.3; edited manually to remove non-generation
high_voltage_providers = {
    'cane sugar production with ethanol by-product',
    'electricity production, deep geothermal',
    'electricity production, hard coal',
    'electricity production, hydro, pumped storage',
    'electricity production, hydro, reservoir, alpine region',
    'electricity production, hydro, reservoir, non-alpine region',
    'electricity production, hydro, reservoir, tropical region',
    'electricity production, hydro, run-of-river',
    'electricity production, lignite',
    'electricity production, natural gas, 10MW',
    'electricity production, natural gas, combined cycle power plant',
    'electricity production, natural gas, conventional power plant',
    'electricity production, nuclear, boiling water reactor',
    'electricity production, nuclear, pressure water reactor',
    'electricity production, nuclear, pressure water reactor, heavy water moderated',
    'electricity production, oil',
    'electricity production, peat',
    'electricity production, wind, 1-3MW turbine, offshore',
    'electricity production, wind, 1-3MW turbine, onshore',
    'electricity production, wind, 2.3MW turbine, precast concrete tower, onshore',
    'electricity production, wind, <1MW turbine, onshore',
    'electricity production, wind, >3MW turbine, onshore',
    'ethanol production from sugarcane',
    'ethanol production from sweet sorghum',
    'ethanol production from wood',
    'heat and power co-generation, biogas, gas engine',
    'heat and power co-generation, diesel, 200kW electrical, SCR-NOx reduction',
    'heat and power co-generation, hard coal',
    'heat and power co-generation, lignite',
    'heat and power co-generation, natural gas, 1MW electrical, lean burn',
    'heat and power co-generation, natural gas, 200kW electrical, lean burn',
    'heat and power co-generation, natural gas, 500kW electrical, lean burn',
    'heat and power co-generation, natural gas, combined cycle power plant, 400MW electrical',
    'heat and power co-generation, natural gas, conventional power plant, 100MW electrical',
    'heat and power co-generation, oil',
    'heat and power co-generation, wood chips, 6667 kW',
    'heat and power co-generation, wood chips, 6667 kW, state-of-the-art 2014',
    'petroleum refinery operation',
    'treatment of bagasse, from sugarcane, in heat and power co-generation unit, 6400kW thermal',
    'treatment of bagasse, from sweet sorghum, in heat and power co-generation unit, 6400kW thermal',
    'treatment of blast furnace gas, in power plant',
    'treatment of coal gas, in power plant',
}

medium_voltage_providers = {
    'burnt shale production',
    'electricity, from municipal waste incineration to generic market for electricity, medium voltage',
    'fluting medium production, semichemical',
    'linerboard production, kraftliner',
    'natural gas, burned in gas turbine, for compressor station',
    'treatment of recovered paper to fluting medium, wellenstoff',
    'treatment of recovered paper to linerboard, testliner',
}

low_voltage_providers = {
    'biogas, burned in micro gas turbine 100kWe',
    'biogas, burned in polymer electrolyte membrane fuel cell 2kWe, future',
    'biogas, burned in solid oxide fuel cell 125kWe, future',
    'biogas, burned in solid oxide fuel cell, with micro gas turbine, 180kWe, future',
    'electricity production, photovoltaic, 3kWp facade installation, multi-Si, laminated, integrated',
    'electricity production, photovoltaic, 3kWp facade installation, multi-Si, panel, mounted',
    'electricity production, photovoltaic, 3kWp facade installation, single-Si, laminated, integrated',
    'electricity production, photovoltaic, 3kWp facade installation, single-Si, panel, mounted',
    'electricity production, photovoltaic, 3kWp flat-roof installation, multi-Si',
    'electricity production, photovoltaic, 3kWp flat-roof installation, single-Si',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, CIS, panel, mounted',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, CdTe, laminated, integrated',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, laminated, integrated',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, laminated, integrated',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, ribbon-Si, laminated, integrated',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, ribbon-Si, panel, mounted',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, laminated, integrated',
    'electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, panel, mounted',
    'electricity production, photovoltaic, 570kWp open ground installation, multi-Si',
    'heat and power co-generation, natural gas, 160kW electrical, Jakobsberg',
    'heat and power co-generation, natural gas, 160kW electrical, lambda=1',
    'heat and power co-generation, natural gas, 50kW electrical, lean burn',
    'heat and power co-generation, natural gas, mini-plant 2KW electrical',
    'sawing and planing, paraná pine, kiln dried',
}

high_voltage_transformation = 'electricity voltage transformation from high to medium voltage'
medium_voltage_transformation = 'electricity voltage transformation from medium to low voltage'

low_voltage_mix = 'market for electricity, low voltage'
medium_voltage_mix = 'market for electricity, medium voltage'
high_voltage_mix = 'market for electricity, high voltage'

all_providers = high_voltage_providers.union(medium_voltage_providers).union(low_voltage_providers)


def set_conversion_to_one_kwh(ds, conversion):
    for exc in ds['exchanges']:
        if exc['activity'] == conversion:
            exc['amount'] = 1


def empty_low_voltage_markets(data):
    is_low_voltage = lambda x: x['name'] == low_voltage_mix

    for ds in get_many(data, is_low_voltage):
        ds['exchanges'] = [exc for exc in ds['exchanges']
                           if exc['activity'] not in all_providers]
        set_conversion_to_one_kwh(ds, medium_voltage_transformation)
    return data


def empty_medium_voltage_markets(data):
    is_medium_voltage = lambda x: x['name'] == medium_voltage_mix

    for ds in get_many(data, is_medium_voltage):
        ds['exchanges'] = [exc for exc in ds['exchanges']
                           if exc['activity'] not in all_providers]
        set_conversion_to_one_kwh(ds, high_voltage_transformation)
    return data


def empty_high_voltage_markets(data):
    is_high_voltage = lambda x: x['name'] == high_voltage_mix

    for ds in get_many(data, is_high_voltage):
        ds['exchanges'] = [exc for exc in ds['exchanges']
                           if exc['activity'] not in all_providers]
    return data
