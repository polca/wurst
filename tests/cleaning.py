from wurst.transformations.cleaning import *


def test_empty_market_dataset():
    given = {
        "exchanges": [
            {
                "name": "market group for transport, freight train",
                "product": "transport, freight train",
                "type": "technosphere",
            },
            {
                "location": "GLO",
                "name": "market for diazine-compound",
                "product": "diazine-compound",
                "type": "production",
            },
            {
                "location": "RER",
                "name": "diazine-compound production",
                "product": "diazine-compound",
                "type": "technosphere",
            },
            {
                "location": "RoW",
                "name": "diazine-compound production",
                "product": "diazine-compound",
                "type": "technosphere",
            },
            {
                "location": "RoW",
                "name": "diazine-compound production",
                "product": "diazine-compound",
                "type": "substitution",
            },
            {
                "location": "RoW",
                "name": "still there",
                "product": "diazine-compound",
                "type": "technosphere",
            },
        ],
        "name": "market for diazine-compound",
        "reference product": "diazine-compound",
    }
    first = {
        "exchanges": [
            {
                "name": "market group for transport, freight train",
                "product": "transport, freight train",
                "type": "technosphere",
            },
            {
                "location": "GLO",
                "name": "market for diazine-compound",
                "product": "diazine-compound",
                "type": "production",
            },
            {
                "location": "RoW",
                "name": "diazine-compound production",
                "product": "diazine-compound",
                "type": "substitution",
            },
            {
                "location": "RoW",
                "name": "still there",
                "product": "diazine-compound",
                "type": "technosphere",
            },
        ],
        "name": "market for diazine-compound",
        "reference product": "diazine-compound",
    }
    second = {
        "exchanges": [
            {
                "name": "market group for transport, freight train",
                "product": "transport, freight train",
                "type": "technosphere",
            },
            {
                "location": "GLO",
                "name": "market for diazine-compound",
                "product": "diazine-compound",
                "type": "production",
            },
            {
                "location": "RoW",
                "name": "diazine-compound production",
                "product": "diazine-compound",
                "type": "substitution",
            },
        ],
        "name": "market for diazine-compound",
        "reference product": "diazine-compound",
    }
    assert empty_market_dataset(given, exclude=["still there"]) == first
    assert empty_market_dataset(given) == second


def test_delete_zero_amount_exchanges():
    given = [
        {
            "exchanges": [
                {"type": "foo", "amount": 0},
                {"type": "bar", "amount": 1},
                {"type": "baz", "amount": 0},
            ]
        }
    ]
    first = [
        {"exchanges": [{"type": "foo", "amount": 0}, {"type": "bar", "amount": 1}]}
    ]
    second = [{"exchanges": [{"type": "bar", "amount": 1}]}]
    assert delete_zero_amount_exchanges(given, drop_types=["baz"]) == first
    assert delete_zero_amount_exchanges(given) == second


def test_remove_exchange_fields_with_nones():
    given = [
        {
            "exchanges": [
                {
                    "name": "market group for transport, freight train",
                    "product": None,
                    "type": "",
                }
            ],
            "name": "market for diazine-compound",
            "reference product": "diazine-compound",
        }
    ]
    expected = [
        {
            "exchanges": [
                {"name": "market group for transport, freight train", "type": ""}
            ],
            "name": "market for diazine-compound",
            "reference product": "diazine-compound",
        }
    ]
    assert remove_exchange_fields_with_nones(given) == expected


def test_add_metadata_to_production_exchanges():
    given = [
        {
            "exchanges": [
                {"name": "D", "unit": "km", "type": "technosphere"},
                {"name": "Y", "unit": "km", "type": "technosphere"},
                {"name": "A", "type": "production"},
                {
                    "name": "Z",
                    "location": "somewhere",
                    "unit": "ton",
                    "type": "production",
                },
            ],
            "name": "A",
            "reference product": "B",
            "location": "C",
            "unit": "kg",
        },
        {
            "exchanges": [],
            "name": "D",
            "reference product": "E",
            "location": "F",
            "unit": "km",
        },
    ]
    expected = [
        {
            "exchanges": [
                {"name": "D", "unit": "km", "location": "F", "type": "technosphere"},
                {"name": "Y", "unit": "km", "type": "technosphere"},
                {"name": "A", "location": "C", "type": "production"},
                {
                    "name": "Z",
                    "location": "somewhere",
                    "unit": "ton",
                    "type": "production",
                },
            ],
            "name": "A",
            "reference product": "B",
            "location": "C",
            "unit": "kg",
        },
        {
            "exchanges": [],
            "name": "D",
            "reference product": "E",
            "location": "F",
            "unit": "km",
        },
    ]
    assert (
        add_metadata_to_production_exchanges(
            given, fields=("location",), matching_fields=("name", "unit")
        )
        == expected
    )
