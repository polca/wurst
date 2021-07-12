import pytest

try:
    from wurst.brightway25 import write_brightway25_database

    # from wurst.brightway import extract_brightway2_databases
    from bw2data import Database, Method, prepare_lca_inputs, get_id
    from bw2data.tests import bw2test
    from bw2calc import LCA
    import numpy as np

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
    # Biosphere database - won't be extracted
    Database("b").write(
        {
            ("b", "1"): {"type": "emission", "exchanges": []},
            ("b", "2"): {"type": "emission", "exchanges": []},
        }
    )

    # Background database - won't be extracted
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

    # Foreground database - will be extracted
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

    Method(("d",)).write([(("b", "1"), 1), (("b", "2"), 1)])


def test_basic_setup(bw25_setup):
    fu, data_objs, _ = prepare_lca_inputs({("c", "2"): 1}, method=("d",))
    lca = LCA(fu, data_objs=data_objs)
    lca.lci()
    lca.lcia()

    print(lca.technosphere_matrix.toarray())
    print(lca.biosphere_matrix.toarray())
    print(lca.supply_array)
    print(lca.score)

    assert np.allclose(lca.score, 44)


def test_bw25_integration_simple(bw25_setup):
    # data = extract_brightway2_databases(["c"])
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
                    "amount": 2000000,  # Should be ignored, not marked as modified
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
                    "amount": 4000000,  # Should be ignored, not marked as modified
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
    write_brightway25_database(modified, "new")  # , add_implicit_production=False)

    fu, data_objs, _ = prepare_lca_inputs({("new", "1"): 1}, method=("d",))
    lca = LCA(fu, data_objs=data_objs)
    lca.lci()
    lca.lcia()

    print(lca.technosphere_matrix.toarray())
    print(lca.biosphere_matrix.toarray())
    print(lca.supply_array)
    print(lca.score)

    assert not np.allclose(lca.score, 44)

    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("a", "2"))],
            lca.dicts.activity[get_id(("c", "1"))],
        ]
        == -2
    )
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("a", "1"))],
            lca.dicts.activity[get_id(("c", "1"))],
        ]
        == -2
    )
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("c", "1"))],
            lca.dicts.activity[get_id(("c", "2"))],
        ]
        == -5
    )
    assert (
        lca.biosphere_matrix[
            lca.dicts.biosphere[get_id(("b", "1"))],
            lca.dicts.activity[get_id(("c", "2"))],
        ]
        == 14
    )
    assert (
        lca.biosphere_matrix[
            lca.dicts.biosphere[get_id(("b", "2"))],
            lca.dicts.activity[get_id(("c", "2"))],
        ]
        == 0
    )
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("c", "2"))],
            lca.dicts.activity[get_id(("new", "1"))],
        ]
        == -1
    )
    assert (
        lca.technosphere_matrix[
            lca.dicts.product[get_id(("new", "1"))],
            lca.dicts.activity[get_id(("new", "1"))],
        ]
        == 1
    )
