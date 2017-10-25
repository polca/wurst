from wurst.transformations.geo import *
import pytest


@pytest.fixture(scope="function")
def defaults():
    data = [{
        'name': 'A', 'reference product': 'B', 'unit': 'C',
        'location': 'SE',
        'exchanges': [{
            'type': 'production', 'amount': 1,
            'production volume': 2,
        }]
    }, {
        'name': 'A', 'reference product': 'B', 'unit': 'C',
        'location': 'NO',
        'exchanges': [{
            'type': 'production', 'amount': 1,
            'production volume': 4,
        }]
    }, {
        'name': 'A', 'reference product': 'B', 'unit': 'C',
        'location': 'RoW',
        'exchanges': [{
            'type': 'production', 'amount': 1,
            'production volume': 14,
        }]
    }, {
        'name': 'D', 'reference product': 'E', 'unit': 'F',
        'location': 'DK',
        'exchanges': [{
            'type': 'production', 'amount': 1,
            'production volume': 1,
        }]
    }]
    ds = {
        'location': ('ecoinvent', 'UN-NEUROPE'),
        'exchanges': [{
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 10,
            'type': 'technosphere',
        }, {
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 100,
            'type': 'technosphere',
        }, {
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 1,
            'type': 'biosphere',
        }]
    }
    return data, ds

def test_relink_defaults(defaults):
    data, ds = defaults
    expected = {
        'location': ('ecoinvent', 'UN-NEUROPE'),
        'exchanges': [{
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 1,
            'type': 'biosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1 / 3 * 10, 'loc': 1 / 3 * 10, 'uncertainty type': 0,
            'location': 'SE',
            'type': 'technosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1 / 3 * 10, 'loc': 1 / 3 * 10, 'uncertainty type': 0,
            'location': 'NO',
            'type': 'technosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1 / 3 * 10, 'loc': 1 / 3 * 10, 'uncertainty type': 0,
            'location': 'RoW',
            'type': 'technosphere',
        }, {
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 100., 'loc': 100., 'uncertainty type': 0,
            'location': 'DK',
            'type': 'technosphere',
        }]
    }
    assert relink_technosphere_exchanges(ds, data) == expected

def test_relink_no_row(defaults):
    data, ds = defaults
    ds['location'] = ('ecoinvent', 'BALTSO')
    data[0]['location'] = 'LT'
    data[1]['location'] = 'LV'
    data[3]['location'] = 'LV'
    data.append({
        'name': 'A', 'reference product': 'B', 'unit': 'C',
        'location': 'EE',
        'exchanges': [{
            'type': 'production', 'amount': 1,
            'production volume': 14,
        }]
    })
    expected = {
        'location': ('ecoinvent', 'BALTSO'),
        'exchanges': [{
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 1,
            'type': 'biosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1, 'loc': 1, 'uncertainty type': 0,
            'location': 'LT',
            'type': 'technosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 2, 'loc': 2, 'uncertainty type': 0,
            'location': 'LV',
            'type': 'technosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 7, 'loc': 7, 'uncertainty type': 0,
            'location': 'EE',
            'type': 'technosphere',
        }, {
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 100., 'loc': 100., 'uncertainty type': 0,
            'location': 'LV',
            'type': 'technosphere',
        }]
    }
    assert relink_technosphere_exchanges(ds, data) == expected

def test_relink_multiple_row(defaults):
    data, ds = defaults
    data.append({
        'name': 'A', 'reference product': 'B', 'unit': 'C',
        'location': 'RoW',
        'exchanges': [{
            'type': 'production', 'amount': 1,
            'production volume': 20,
        }]
    })
    expected = {
        'location': ('ecoinvent', 'UN-NEUROPE'),
        'exchanges': [{
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 1,
            'type': 'biosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1 / 4 * 10, 'loc': 1 / 4 * 10, 'uncertainty type': 0,
            'location': 'SE',
            'type': 'technosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1 / 4 * 10, 'loc': 1 / 4 * 10, 'uncertainty type': 0,
            'location': 'NO',
            'type': 'technosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1 / 4 * 10, 'loc': 1 / 4 * 10, 'uncertainty type': 0,
            'location': 'RoW',
            'type': 'technosphere',
        }, {
            'name': 'A', 'product': 'B', 'unit': 'C',
            'amount': 1 / 4 * 10, 'loc': 1 / 4 * 10, 'uncertainty type': 0,
            'location': 'RoW',
            'type': 'technosphere',
        }, {
            'name': 'D', 'product': 'E', 'unit': 'F',
            'amount': 100., 'loc': 100., 'uncertainty type': 0,
            'location': 'DK',
            'type': 'technosphere',
        }]
    }
    assert relink_technosphere_exchanges(ds, data) == expected

def test_relink_only_glo(defaults):
    pass

def test_relink_non_exclusive(defaults):
    pass

def test_relink_invalid_error(defaults):
    pass

def test_relink_invalid_drop(defaults):
    pass

def test_relink_smallest_first(defaults):
    pass

def test_relink_intersects(defaults):
    pass
