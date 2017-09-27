from wurst.ecoinvent.electricity_markets import *


def test_empty_low_voltage_markets():
    given = [{
        'exchanges': [{
                'name': 'market for transmission network, electricity, low voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'market for sulfur hexafluoride, liquid',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.0096,
                'name': 'market for electricity, low voltage',
                'type': 'technosphere',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.0,
                'name': 'market for electricity, low voltage',
                'type': 'production',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.2,
                'name': 'electricity voltage transformation from medium to low voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted',
                'unit': 'kilowatt hour',
            }, {
                'name': 'burnt shale production',
                'unit': 'kilowatt hour',
            }, {
                'name': 'petroleum refinery operation',
                'unit': 'kilowatt hour',
        }],
        'name': 'market for electricity, low voltage',
    }]
    expected = [{
        'exchanges': [{
                'name': 'market for transmission network, electricity, low voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'market for sulfur hexafluoride, liquid',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.0096,
                'name': 'market for electricity, low voltage',
                'type': 'technosphere',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.0,
                'name': 'market for electricity, low voltage',
                'type': 'production',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.,
                'name': 'electricity voltage transformation from medium to low voltage',
                'unit': 'kilowatt hour',
        }],
        'name': 'market for electricity, low voltage',
    }]
    assert empty_low_voltage_markets(given) == expected

def test_empty_medium_voltage_markets():
    given = [{
        'exchanges': [{
                'name': 'market for transmission network, electricity, medium voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'market for sulfur hexafluoride, liquid',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.0096,
                'name': 'market for electricity, medium voltage',
                'type': 'technosphere',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.0,
                'name': 'market for electricity, medium voltage',
                'type': 'production',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.2,
                'name': 'electricity voltage transformation from high to medium voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted',
                'unit': 'kilowatt hour',
            }, {
                'name': 'burnt shale production',
                'unit': 'kilowatt hour',
            }, {
                'name': 'petroleum refinery operation',
                'unit': 'kilowatt hour',
        }],
        'name': 'market for electricity, medium voltage',
    }]
    expected = [{
        'exchanges': [{
                'name': 'market for transmission network, electricity, medium voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'market for sulfur hexafluoride, liquid',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.0096,
                'name': 'market for electricity, medium voltage',
                'type': 'technosphere',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.0,
                'name': 'market for electricity, medium voltage',
                'type': 'production',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.,
                'name': 'electricity voltage transformation from high to medium voltage',
                'unit': 'kilowatt hour',
        }],
        'name': 'market for electricity, medium voltage',
    }]
    assert empty_medium_voltage_markets(given) == expected

def test_empty_high_voltage_markets():
    given = [{
        'exchanges': [{
                'name': 'market for transmission network, electricity, high voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'market for sulfur hexafluoride, liquid',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.0096,
                'name': 'market for electricity, high voltage',
                'type': 'technosphere',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.0,
                'name': 'market for electricity, high voltage',
                'type': 'production',
                'unit': 'kilowatt hour',
            }, {
                'name': 'electricity, high voltage, import from CA-AB',
                'unit': 'kilowatt hour',
            }, {
                'name': 'electricity, high voltage, import from WECC, US only',
                'unit': 'kilowatt hour',
            }, {
                'name': 'electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted',
                'unit': 'kilowatt hour',
            }, {
                'name': 'burnt shale production',
                'unit': 'kilowatt hour',
            }, {
                'name': 'petroleum refinery operation',
                'unit': 'kilowatt hour',
        }],
        'name': 'market for electricity, high voltage',
    }]
    expected = [{
        'exchanges': [{
                'name': 'market for transmission network, electricity, high voltage',
                'unit': 'kilowatt hour',
            }, {
                'name': 'market for sulfur hexafluoride, liquid',
                'unit': 'kilowatt hour',
            }, {
                'amount': 0.0096,
                'name': 'market for electricity, high voltage',
                'type': 'technosphere',
                'unit': 'kilowatt hour',
            }, {
                'amount': 1.0,
                'name': 'market for electricity, high voltage',
                'type': 'production',
                'unit': 'kilowatt hour',
        }],
        'name': 'market for electricity, high voltage',
    }]
    assert empty_high_voltage_markets(given) == expected
