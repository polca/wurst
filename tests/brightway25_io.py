"""Tests for Brightway 2.5 database writing functionality.

These tests verify that modified datasets and exchanges are correctly written
to Brightway 2.5 databases using delta/override functionality.
"""
import pytest

try:
    import numpy as np
    from bw2calc import LCA
    from bw2data import Database, Method, get_id, prepare_lca_inputs
    from bw2data.tests import bw2test

    from wurst.brightway25 import write_brightway25_database

    bw25 = True
except ImportError:
    bw25 = False

    def bw2test(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper


if not bw25:
    pytest.skip("Brightway 2.5 not installed", allow_module_level=True)


@pytest.fixture
@bw2test
def bw25_setup():
    """Set up test databases for Brightway 2.5 testing.

    Creates three databases:
    - 'b': Biosphere database with emissions
    - 'a': Background technosphere database
    - 'c': Foreground database that will be modified

    The baseline calculation for (c, 2) has a total impact of 44.
    """
    # Biosphere database - emissions
    Database("b").write(
        {
            ("b", "1"): {"type": "emission", "exchanges": []},
            ("b", "2"): {"type": "emission", "exchanges": []},
        }
    )

    # Background database - links to a
    Database("a").write(
        {
            ("a", "1"): {
                "exchanges": [
                    {"input": ("a", "1"), "amount": 1, "type": "production"},
                    {"input": ("b", "1"), "amount": 1, "type": "biosphere"},
                ]
            },
            ("a", "2"): {
                "exchanges": [
                    {"input": ("a", "2"), "amount": 1, "type": "production"},
                    {"input": ("b", "2"), "amount": 2, "type": "biosphere"},
                    {"input": ("a", "1"), "amount": 1, "type": "technosphere"},
                ]
            },
        }
    )

    # Foreground database - will be modified
    Database("c").write(
        {
            ("c", "1"): {
                "name": "c1-1",
                "location": "c1-2",
                "unit": "c1-3",
                "exchanges": [
                    {"input": ("c", "1"), "amount": 1, "type": "production"},
                    {"input": ("a", "1"), "amount": 1, "type": "technosphere"},
                    {"input": ("a", "2"), "amount": 2, "type": "technosphere"},
                    {"input": ("b", "1"), "amount": 4, "type": "biosphere"},
                ],
            },
            ("c", "2"): {
                "name": "c2-1",
                "location": "c2-2",
                "unit": "c2-3",
                "exchanges": [
                    {"input": ("c", "2"), "amount": 1, "type": "production"},
                    {"input": ("a", "1"), "amount": 1, "type": "technosphere"},
                    {"input": ("a", "2"), "amount": 2, "type": "technosphere"},
                    {"input": ("c", "1"), "amount": 3, "type": "technosphere"},
                    {"input": ("b", "1"), "amount": 4, "type": "biosphere"},
                ],
            },
        }
    )

    """
    Base technosphere matrix:

              a1  a2  c1  c2
        a1 [[ 1. -1. -1. -1.]
        a2  [ 0.  1. -2. -2.]
        c1  [ 0.  0.  1. -3.]
        c2  [ 0.  0.  0.  1.]]

    Base biosphere matrix:

             a1 a2 c1 c2
        b1 [[1. 0. 4. 4.]
        b2  [0. 2. 0. 0.]]

    Total impact for c2 is 1*4 + (3*4) + (2 + 3*2) * 2 + (1 + 3*1 + 2*1 + 3*2*1) * 1 = 44

    """

    # Method with unit CF for both emissions
    Method(("d",)).write([(("b", "1"), 1), (("b", "2"), 1)])


def test_basic_setup(bw25_setup):
    """Test that the baseline LCA calculation works correctly.

    Verifies that the fixture setup produces the expected baseline impact
    score of 44 for activity (c, 2).
    """
    func_unit = {("c", "2"): 1}
    method = ("d",)

    fu, data_objs, _ = prepare_lca_inputs(func_unit, method=method)
    lca = LCA(fu, data_objs=data_objs)
    lca.lci()
    lca.lcia()

    # Baseline impact calculation should equal 44
    # This verifies the test setup is correct
    assert np.allclose(lca.score, 44), f"Baseline score should be 44, got {lca.score}"


def test_bw25_integration_simple(bw25_setup):
    """Test that modified exchanges and new activities are correctly written.

    This test verifies that:
    1. Modified exchanges (marked with modified=True) override original values
    2. Unmodified exchanges are ignored (not written)
    3. New activities can be added
    4. The overrides work correctly in LCA calculations
    """
    # Create modified dataset where:
    # - Activity c1: Modified exchange to a1 (amount changed from 1 to 2)
    # - Activity c2: Modified exchanges to c1 (amount changed from 3 to 5)
    #                and to b1 (amount changed from 4 to 14)
    # - Activity c3: New activity
    modified = [
        {
            "location": "c1-2",
            "database": "c",
            "code": "1",
            "name": "c1-1",
            "reference product": "",
            "unit": "c1-3",
            "exchanges": [
                {
                    "amount": 1,
                    "type": "production",
                    "database": "c",
                    "name": "c1-1",
                    "location": "c1-2",
                    "unit": "c1-3",
                    "product": "",
                },
                {
                    "amount": 2,
                    "modified": True,
                    "type": "technosphere",
                    "input": ("a", "1"),
                    "database": "a",
                },
                {
                    "amount": 2000000,  # Not marked as modified - should be ignored
                    "uncertainty type": 0,
                    "loc": 2,
                    "type": "technosphere",
                    "production volume": None,
                    "input": ("a", "2"),
                    "name": None,
                    "product": "",
                    "unit": None,
                    "location": None,
                    "database": "a",
                },
            ],
        },
        {
            "location": "c2-2",
            "database": "c",
            "code": "2",
            "name": "c2-1",
            "reference product": "",
            "unit": "c2-3",
            "exchanges": [
                {
                    "amount": 1,
                    "type": "production",
                    "database": "c",
                    "name": "c2-1",
                    "location": "c2-2",
                    "unit": "c2-3",
                    "product": "",
                },
                {
                    "amount": 5,
                    "type": "technosphere",
                    "product": "",
                    "name": "c1-1",
                    "unit": "c1-3",
                    "location": "c1-2",
                    "modified": True,
                    "database": "c",
                },
                {
                    "amount": 14,
                    "type": "biosphere",
                    "input": ("b", "1"),
                    "database": "b",
                    "modified": True,
                },
                {
                    "amount": 4000000,  # Not marked as modified - should be ignored
                    "type": "biosphere",
                    "input": ("b", "2"),
                    "database": "b",
                },
            ],
        },
        {
            "location": "c3-2",
            "database": "c",
            "modified": True,
            "code": "1",
            "name": "c3-1",
            "reference product": "",
            "unit": "c3-3",
            "exchanges": [
                {
                    "amount": 1,
                    "type": "technosphere",
                    "product": "",
                    "database": "c",
                    "name": "c2-1",
                    "unit": "c2-3",
                    "location": "c2-2",
                },
                {
                    "amount": 1,
                    "type": "production",
                    "name": "c3-1",
                    "database": None,
                    "product": "",
                    "unit": "c3-3",
                    "location": "c3-2",
                },
            ],
        },
    ]
    # Write the modified database
    write_brightway25_database(modified, "new")

    # Calculate LCA for the new activity
    func_unit = {("new", "1"): 1}
    fu, data_objs, _ = prepare_lca_inputs(func_unit, method=("d",))
    lca = LCA(fu, data_objs=data_objs)
    lca.lci()
    lca.lcia()

    # The score should be different from the baseline due to modifications
    assert not np.allclose(
        lca.score, 44
    ), "Score should differ from baseline after modifications"

    # Verify modified exchange: (c,1) gets a2 with amount -2 (unchanged from baseline)
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("a", "2"))],
            lca.dicts.activity[get_id(("c", "1"))],
        ]
        == -2
    ), "Exchange (a,2) -> (c,1) should be -2"

    # Verify modified exchange: (c,1) gets a1 with amount -2 (modified from -1)
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("a", "1"))],
            lca.dicts.activity[get_id(("c", "1"))],
        ]
        == -2
    ), "Exchange (a,1) -> (c,1) should be modified to -2"

    # Verify modified exchange: (c,2) gets c1 with amount -5 (modified from -3)
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("c", "1"))],
            lca.dicts.activity[get_id(("c", "2"))],
        ]
        == -5
    ), "Exchange (c,1) -> (c,2) should be modified to -5"

    # Verify modified biosphere exchange: (c,2) emits b1 with amount 14 (modified from 4)
    assert (
        lca.biosphere_matrix[
            lca.dicts.biosphere[get_id(("b", "1"))],
            lca.dicts.activity[get_id(("c", "2"))],
        ]
        == 14
    ), "Biosphere exchange (b,1) -> (c,2) should be modified to 14"

    # Verify unmodified exchange still has original value (not overridden)
    assert (
        lca.biosphere_matrix[
            lca.dicts.biosphere[get_id(("b", "2"))],
            lca.dicts.activity[get_id(("c", "2"))],
        ]
        == 0
    ), "Unmodified biosphere exchange should retain original value"

    # Verify new activity: (new,1) gets c2 with amount -1
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("c", "2"))],
            lca.dicts.activity[get_id(("new", "1"))],
        ]
        == -1
    ), "New activity (new,1) should have exchange to (c,2) with amount -1"

    # Verify new activity has production exchange
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("new", "1"))],
            lca.dicts.activity[get_id(("new", "1"))],
        ]
        == 1
    ), "New activity should have production exchange with amount 1"


def test_database_name_collision_error(bw25_setup):
    """Test that creating a database with an existing name raises an error.

    This covers line 62 in brightway25/__init__.py: assert name not in bd.databases
    """
    modified = [
        {
            "location": "c1-2",
            "database": "c",
            "code": "1",
            "name": "c1-1",
            "reference product": "",
            "unit": "c1-3",
            "modified": True,
            "exchanges": [
                {
                    "amount": 1,
                    "type": "production",
                    "name": "c1-1",
                    "reference product": "",
                    "product": "",
                    "location": "c1-2",
                    "unit": "c1-3",
                    "database": "c",
                },
                {
                    "amount": 1,
                    "type": "technosphere",
                    "input": ("a", "1"),
                    "database": "a",
                },
            ],
        }
    ]

    # First write should succeed
    write_brightway25_database(modified, "test_db_collision")

    # Verify database was created
    import bw2data as bd

    assert "test_db_collision" in bd.databases

    # Second write with same name should fail
    with pytest.raises(AssertionError, match="This database already exists"):
        write_brightway25_database(modified, "test_db_collision")


def test_brightway25_with_metadata(bw25_setup):
    """Test that write_brightway25_database accepts and stores metadata.

    This covers the metadata parameter in brightway25/__init__.py line 83.
    """
    import bw2data as bd

    # Create a simple modified dataset
    modified = [
        {
            "location": "GLO",
            "database": "c",
            "code": "3",
            "name": "test_activity",
            "reference product": "test_product",
            "unit": "kg",
            "modified": True,
            "exchanges": [
                {
                    "amount": 1,
                    "type": "production",
                    "name": "test_activity",
                    "product": "test_product",
                    "location": "GLO",
                    "unit": "kg",
                    "reference product": "test_product",
                    "database": "c",
                },
                {
                    "amount": 2,
                    "type": "technosphere",
                    "input": ("a", "1"),
                    "database": "a",
                    "modified": True,
                },
            ],
        }
    ]

    # Define custom metadata
    metadata = {
        "description": "Test database with metadata",
        "version": "2.0",
        "author": "test_user_25",
    }

    # Write database with metadata
    write_brightway25_database(modified, "test_meta_25", metadata=metadata)

    # Verify database was created
    assert "test_meta_25" in bd.databases

    # Retrieve database and check metadata was stored
    db = bd.Database("test_meta_25")
    assert "description" in db.metadata
    assert db.metadata["description"] == "Test database with metadata"
    assert db.metadata["version"] == "2.0"
    assert db.metadata["author"] == "test_user_25"


# ============================================================================
# MISSING TEST COVERAGE
# ============================================================================
#
# The following code paths in src/wurst/brightway25/__init__.py are NOT tested:
#
# 1. Parameters handling (lines 68-71):
#    - if "parameters" in ds: conversion to Brightway2 format
#    - Need to test that dataset parameters are correctly converted
#
# 2. Error cases (lines 78-79):
#    - check_internal_linking(data) - InvalidLink exceptions
#    - check_duplicate_codes(new_activities) - NonuniqueCode exceptions
#    - Need tests for both error conditions
#
# 3. Different exchange types (line 132):
#    - flip = exc["type"] not in PRODUCTION
#    - Currently only tests "technosphere" and "biosphere"
#    - Missing: "substitution", "generic production" exchange types
#
# 4. Edge cases:
#    - Activities with empty exchanges list
#    - Activities modified but with no modified exchanges
#    - Mixed modified/unmodified exchanges in same activity
#    - Exchange with wrong input reference
#
# TESTED (NOW COVERED):
# ✓ Database name collision (line 62)
# ✓ Metadata parameter in write_brightway25_database (line 83)
#
# ============================================================================
