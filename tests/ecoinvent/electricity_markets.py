from wurst.ecoinvent.electricity_markets import *


def test_empty_low_voltage_markets():
    given = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, low voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, low voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, low voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.2,
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted",
                    "unit": "kilowatt hour",
                },
                {"name": "burnt shale production", "unit": "kilowatt hour"},
                {"name": "petroleum refinery operation", "unit": "kilowatt hour"},
            ],
            "name": "market for electricity, low voltage",
        }
    ]
    expected = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, low voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, low voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, low voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                },
            ],
            "name": "market for electricity, low voltage",
        }
    ]
    assert empty_low_voltage_markets(given) == expected


def test_empty_medium_voltage_markets():
    given = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, medium voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, medium voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.2,
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted",
                    "unit": "kilowatt hour",
                },
                {"name": "burnt shale production", "unit": "kilowatt hour"},
                {"name": "petroleum refinery operation", "unit": "kilowatt hour"},
            ],
            "name": "market for electricity, medium voltage",
        }
    ]
    expected = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, medium voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, medium voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                },
            ],
            "name": "market for electricity, medium voltage",
        }
    ]
    assert empty_medium_voltage_markets(given) == expected


def test_empty_high_voltage_markets():
    given = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, high voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, high voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, high voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity, high voltage, import from CA-AB",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity, high voltage, import from WECC, US only",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted",
                    "unit": "kilowatt hour",
                },
                {"name": "burnt shale production", "unit": "kilowatt hour"},
                {"name": "petroleum refinery operation", "unit": "kilowatt hour"},
            ],
            "name": "market for electricity, high voltage",
        }
    ]
    expected = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, high voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, high voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, high voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
            ],
            "name": "market for electricity, high voltage",
        }
    ]
    assert empty_high_voltage_markets(given) == expected


def test_move_all_generation_to_high_voltage():
    given = [
        {
            "location": "CZ",
            "name": "market for electricity, low voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "amount": 6,
                    "type": "technosphere",
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilogram",
                    "location": "RER",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.02,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.01,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.9,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "product": "electricity, low voltage",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 2,
                    "amount": 9,
                    "type": "biosphere",
                    "name": "Sulfur hexafluoride",
                    "unit": "kilogram",
                    "location": None,
                    "categories": ("air",),
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, medium voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 1.8,
                    "type": "technosphere",
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "production",
                    "product": "electricity, medium voltage",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.9,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1,
                    "type": "technosphere",
                    "name": "electricity, from municipal waste incineration to generic market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1234,
                    "type": "technosphere",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.3,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from AT",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from DE",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
    ]
    expected = [
        {
            "location": "CZ",
            "name": "market for electricity, low voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "amount": 6,
                    "type": "technosphere",
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilogram",
                    "location": "RER",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "product": "electricity, low voltage",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 2,
                    "amount": 9,
                    "type": "biosphere",
                    "name": "Sulfur hexafluoride",
                    "unit": "kilogram",
                    "location": None,
                    "categories": ("air",),
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, medium voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 1.8,
                    "type": "technosphere",
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "production",
                    "product": "electricity, medium voltage",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1234,
                    "type": "technosphere",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4 * 0.9 * 0.9,
                    "loc": 0.4 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.243,  # 0.3 * 0.9 * 0.9,
                    "loc": 0.243,  # 0.3 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05 * 0.9 * 0.9,
                    "loc": 0.05 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from AT",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05 * 0.9 * 0.9,
                    "loc": 0.05 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from DE",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1 * 0.9,
                    "loc": 0.1 * 0.9,
                    "type": "technosphere",
                    "name": "electricity, from municipal waste incineration to generic market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.02,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.01,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
    ]
    assert move_all_generation_to_high_voltage(given) == expected


def test_remove_electricity_trade():
    given = [
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.3,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from AT",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from DE",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        }
    ]
    expected = [
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.3,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        }
    ]
    assert remove_electricity_trade(given) == expected
