from brightway_fixtures import test_bw2_database

if test_bw2_database is not None:
    from wurst.brightway import extract_brightway2_databases
    from bw2data.tests import bw2test
    from bw2data import Database
    import pytest

    def test_extraction(test_bw2_database):
        expected = [
            {
                "classifications": [42],
                "code": "1",
                "comment": "Yep",
                "database": "food",
                "exchanges": [
                    {
                        "name": "dinner",
                        "amount": 0.5,
                        "database": "food",
                        "loc": 0.5,
                        "location": "CH",
                        "product": None,
                        "production volume": 13,
                        "type": "technosphere",
                        "uncertainty type": 0,
                        "unit": "kg",
                    },
                    {
                        "name": "an emission",
                        "amount": 0.05,
                        "categories": ["things"],
                        "input": ("biosphere", "1"),
                        "database": "biosphere",
                        "location": None,
                        "product": "find me!",
                        "production volume": None,
                        "type": "biosphere",
                        "uncertainty type": 4,
                        "unit": "kg",
                    },
                ],
                "location": "CA",
                "name": "lunch",
                "reference product": "stuff",
                "unit": "kg",
                "parameters": {"losses_gross_net": 0.01},
                "parameters full": [{"amount": 0.01, "name": "losses_gross_net"}],
            },
            {
                "classifications": [],
                "code": "2",
                "comment": "",
                "database": "food",
                "exchanges": [
                    {
                        "name": "lunch",
                        "amount": 0.25,
                        "location": "CA",
                        "product": "stuff",
                        "database": "food",
                        "production volume": None,
                        "type": "technosphere",
                        "uncertainty type": 0,
                        "unit": "kg",
                    },
                    {
                        "name": "another emission",
                        "amount": 0.15,
                        "categories": ["things"],
                        "input": ("biosphere", "2"),
                        "database": "biosphere",
                        "location": None,
                        "product": None,
                        "production volume": None,
                        "type": "biosphere",
                        "uncertainty type": 0,
                        "unit": "kg",
                    },
                ],
                "location": "CH",
                "name": "dinner",
                "reference product": None,
                "unit": "kg",
                "parameters": {"rara": 13},
                "parameters full": [
                    {"name": "rara", "amount": 13, "something": "else"}
                ],
            },
        ]

        assert sorted(
            extract_brightway2_databases("food"), key=lambda x: x["code"]
        ) == sorted(expected, key=lambda x: x["code"])

    @bw2test
    def test_extraction_missing_database():
        with pytest.raises(AssertionError):
            assert extract_brightway2_databases("biosphere3")

    def test_extraction_input_formats(test_bw2_database):
        assert extract_brightway2_databases("food")
        assert extract_brightway2_databases(["food"])
        assert extract_brightway2_databases(("food",))
        assert extract_brightway2_databases({"food"})
        with pytest.raises(AssertionError):
            assert extract_brightway2_databases({"food": None})

    def test_extraction_with_properties():
        data = extract_brightway2_databases("food")
        assert all("properties" not in exc for ds in data for exc in ds["exchanges"])
        data = extract_brightway2_databases("food", add_properties=True)
        assert all("properties" in exc for ds in data for exc in ds["exchanges"])

    def test_extraction_with_identifiers():
        data = extract_brightway2_databases("food")
        assert all("properties" not in exc for ds in data for exc in ds["exchanges"])
        data = extract_brightway2_databases("food", add_identifiers=True)
        assert all("id" in ds for ds in data)
        assert all("id" in exc for ds in data for exc in ds["exchanges"])
        assert all("code" in exc for ds in data for exc in ds["exchanges"])

else:
    pass
