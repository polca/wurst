try:
    from bw2data.tests import bw2test
    from bw2data import Database
    import pytest

    biosphere = {
        ("biosphere", "1"): {
            "categories": ["things"],
            "code": "1",
            "exchanges": [],
            "reference product": "find me!",
            "name": "an emission",
            "type": "emission",
            "unit": "kg",
        },
        ("biosphere", "2"): {
            "categories": ["things"],
            "code": "2",
            "exchanges": [],
            "type": "emission",
            "name": "another emission",
            "unit": "kg",
        },
    }

    food = {
        ("food", "1"): {
            "categories": ["stuff", "meals"],
            "code": "1",
            "classifications": [42],
            "comment": "Yep",
            "reference product": "stuff",
            "exchanges": [
                {
                    "amount": 0.5,
                    "input": ("food", "2"),
                    "type": "technosphere",
                    "production volume": 13,
                },
                {
                    "amount": 0.05,
                    "input": ("biosphere", "1"),
                    "type": "biosphere",
                    "uncertainty type": 4,
                },
            ],
            "location": "CA",
            "name": "lunch",
            "type": "process",
            "unit": "kg",
            "parameters": {"losses_gross_net": {"amount": 0.01}},
        },
        ("food", "2"): {
            "categories": ["stuff", "meals"],
            "code": "2",
            "exchanges": [
                {
                    "amount": 0.25,
                    "input": ("food", "1"),
                    "type": "technosphere",
                    "uncertainty type": 0,
                },
                {
                    "amount": 0.15,
                    "input": ("biosphere", "2"),
                    "type": "biosphere",
                    "uncertainty type": 0,
                },
            ],
            "location": "CH",
            "name": "dinner",
            "type": "process",
            "unit": "kg",
            "parameters": [{"name": "rara", "amount": 13, "something": "else"}],
        },
    }

    @pytest.fixture(scope="function")
    @bw2test
    def test_bw2_database():
        d = Database("biosphere")
        d.write(biosphere)
        d = Database("food")
        d.write(food)


except ImportError:
    test_bw2_database = None
