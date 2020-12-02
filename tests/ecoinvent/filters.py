from wurst.ecoinvent.filters import _oil
from wurst import get_many


def test_oil():
    given = [
        {"name": "electricity production, oil, aluminium industry"},
        {"name": "electricity production, oil"},
        {"name": "electricity production, nuclear, boiling water reactor"},
    ]
    expected = [
        {"name": "electricity production, oil, aluminium industry"},
        {"name": "electricity production, oil"},
    ]
    assert list(get_many(given, _oil)) == expected
