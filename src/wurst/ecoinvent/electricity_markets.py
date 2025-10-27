from .. import toolz
from ..searching import get_many, equals
from ..transformations import rescale_exchange
from functools import partial


def get_generators_in_mix(db, name="market for electricity, high voltage"):
    """Get names of inputs to electricity mixes"""
    inputs = set()
    for act in db:
        if act["name"] == name:
            for exc in act.technosphere():
                producer = exc.input
                if producer["unit"] == "kilowatt hour":
                    inputs.add(producer["name"])
    return inputs


# Valid as of 3.3; edited manually to remove non-generation
high_voltage_providers = {
    "cane sugar production with ethanol by-product",
    "electricity production, deep geothermal",
    "electricity production, hard coal",
    "electricity production, hydro, pumped storage",
    "electricity production, hydro, reservoir, alpine region",
    "electricity production, hydro, reservoir, non-alpine region",
    "electricity production, hydro, reservoir, tropical region",
    "electricity production, hydro, run-of-river",
    "electricity production, lignite",
    "electricity production, natural gas, 10MW",
    "electricity production, natural gas, combined cycle power plant",
    "electricity production, natural gas, conventional power plant",
    "electricity production, nuclear, boiling water reactor",
    "electricity production, nuclear, pressure water reactor",
    "electricity production, nuclear, pressure water reactor, heavy water moderated",
    "electricity production, oil",
    "electricity production, peat",
    "electricity production, wind, 1-3MW turbine, offshore",
    "electricity production, wind, 1-3MW turbine, onshore",
    "electricity production, wind, 2.3MW turbine, precast concrete tower, onshore",
    "electricity production, wind, <1MW turbine, onshore",
    "electricity production, wind, >3MW turbine, onshore",
    "ethanol production from sugarcane",
    "ethanol production from sweet sorghum",
    "ethanol production from wood",
    "heat and power co-generation, biogas, gas engine",
    "heat and power co-generation, diesel, 200kW electrical, SCR-NOx reduction",
    "heat and power co-generation, hard coal",
    "heat and power co-generation, lignite",
    "heat and power co-generation, natural gas, 1MW electrical, lean burn",
    "heat and power co-generation, natural gas, 200kW electrical, lean burn",
    "heat and power co-generation, natural gas, 500kW electrical, lean burn",
    "heat and power co-generation, natural gas, combined cycle power plant, 400MW electrical",
    "heat and power co-generation, natural gas, conventional power plant, 100MW electrical",
    "heat and power co-generation, oil",
    "heat and power co-generation, wood chips, 6667 kW",
    "heat and power co-generation, wood chips, 6667 kW, state-of-the-art 2014",
    "petroleum refinery operation",
    "treatment of bagasse, from sugarcane, in heat and power co-generation unit, 6400kW thermal",
    "treatment of bagasse, from sweet sorghum, in heat and power co-generation unit, 6400kW thermal",
    "treatment of blast furnace gas, in power plant",
    "treatment of coal gas, in power plant",
    # New in 3.5
    "electricity production, hard coal, conventional",
    "electricity production, hard coal, supercritical",
    "electricity production, solar thermal parabolic trough, 50 MW",
    "electricity production, solar tower power plant, 20 MW",
}

medium_voltage_providers = {
    "burnt shale production",
    "electricity, from municipal waste incineration to generic market for electricity, medium voltage",
    "fluting medium production, semichemical",
    "linerboard production, kraftliner",
    "natural gas, burned in gas turbine, for compressor station",
    "treatment of recovered paper to fluting medium, wellenstoff",
    "treatment of recovered paper to linerboard, testliner",
}

low_voltage_providers = {
    "biogas, burned in micro gas turbine 100kWe",
    "biogas, burned in polymer electrolyte membrane fuel cell 2kWe, future",
    "biogas, burned in solid oxide fuel cell 125kWe, future",
    "biogas, burned in solid oxide fuel cell, with micro gas turbine, 180kWe, future",
    "electricity production, photovoltaic, 3kWp facade installation, multi-Si, laminated, integrated",
    "electricity production, photovoltaic, 3kWp facade installation, multi-Si, panel, mounted",
    "electricity production, photovoltaic, 3kWp facade installation, single-Si, laminated, integrated",
    "electricity production, photovoltaic, 3kWp facade installation, single-Si, panel, mounted",
    "electricity production, photovoltaic, 3kWp flat-roof installation, multi-Si",
    "electricity production, photovoltaic, 3kWp flat-roof installation, single-Si",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, CIS, panel, mounted",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, CdTe, laminated, integrated",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, laminated, integrated",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, laminated, integrated",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, ribbon-Si, laminated, integrated",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, ribbon-Si, panel, mounted",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, laminated, integrated",
    "electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, panel, mounted",
    "electricity production, photovoltaic, 570kWp open ground installation, multi-Si",
    "heat and power co-generation, natural gas, 160kW electrical, Jakobsberg",
    "heat and power co-generation, natural gas, 160kW electrical, lambda=1",
    "heat and power co-generation, natural gas, 50kW electrical, lean burn",
    "heat and power co-generation, natural gas, mini-plant 2KW electrical",
    "sawing and planing, paraná pine, kiln dried",
}

high_voltage_transformation = (
    "electricity voltage transformation from high to medium voltage"
)
medium_voltage_transformation = (
    "electricity voltage transformation from medium to low voltage"
)

low_voltage_mix = "market for electricity, low voltage"
medium_voltage_mix = "market for electricity, medium voltage"
high_voltage_mix = "market for electricity, high voltage"

all_providers = high_voltage_providers.union(medium_voltage_providers).union(
    low_voltage_providers
)


def move_all_generation_to_high_voltage(data):
    """Move all generation sources to the high voltage market.

    Uses the relative shares in the low voltage market, **ignoring transmission losses**. In theory, using the production volumes would be more correct, but these numbers are no longer updated since ecoinvent 3.2.

    Empties out the medium and low voltage mixes."""
    MIXES = {low_voltage_mix, medium_voltage_mix, high_voltage_mix}
    mix_filter = lambda ds: ds["name"] in MIXES
    for group in toolz.groupby("location", filter(mix_filter, data)).values():
        assert len(group) == 3
        high, low, medium = sorted(group, key=lambda x: x["name"])
        medium_in_low = [
            ex for ex in low["exchanges"] if ex["name"] == medium_voltage_transformation
        ][0]["amount"]
        high_in_low = [
            ex
            for ex in medium["exchanges"]
            if ex["name"] == high_voltage_transformation
        ][0]["amount"] * medium_in_low
        for exc in high["exchanges"]:
            if exc["name"] in high_voltage_providers or (
                "electricity" in exc["name"] and "import from" in exc["name"]
            ):
                rescale_exchange(exc, high_in_low)
        high["exchanges"].extend(
            [
                rescale_exchange(exc, medium_in_low)
                for exc in medium["exchanges"]
                if exc["name"] in medium_voltage_providers
            ]
        )
        high["exchanges"].extend(
            [exc for exc in low["exchanges"] if exc["name"] in low_voltage_providers]
        )
    data = empty_medium_voltage_markets(data)
    data = empty_low_voltage_markets(data)
    return data


def remove_electricity_trade(data):
    """Delete all electricity trade exchanges.

    Intended to be used when substituting in new trade mixes."""
    MIXES = {low_voltage_mix, medium_voltage_mix, high_voltage_mix}
    mix_filter = lambda ds: ds["name"] in MIXES
    for ds in filter(mix_filter, data):
        ds["exchanges"] = [
            exc
            for exc in ds["exchanges"]
            if not ("electricity" in exc["name"] and "import from" in exc["name"])
        ]
    return data


def include_filter(exc):
    return exc["unit"] != "kilowatt hour" or (
        "import from" not in exc["name"] and exc["name"] not in all_providers
    )


def set_conversion_to_one_kwh(ds, conversion):
    for exc in ds["exchanges"]:
        if exc["name"] == conversion:
            exc["amount"] = 1


def _empty(data, kind):
    for ds in get_many(data, equals("name", kind)):
        ds["exchanges"] = list(filter(include_filter, ds["exchanges"]))

        if kind == low_voltage_mix:
            set_conversion_to_one_kwh(ds, medium_voltage_transformation)
        elif kind == medium_voltage_mix:
            set_conversion_to_one_kwh(ds, high_voltage_transformation)

    return data


empty_low_voltage_markets = partial(_empty, kind=low_voltage_mix)
empty_medium_voltage_markets = partial(_empty, kind=medium_voltage_mix)
empty_high_voltage_markets = partial(_empty, kind=high_voltage_mix)
