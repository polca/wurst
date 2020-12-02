from numbers import Number


def rescale_exchange(exc, value, remove_uncertainty=True):
    """Dummy function to rescale exchange amount and uncertainty.

    This depends on some code being separated from Ocelot, which will take a bit of time.

    * ``exc`` is an exchange dataset.
    * ``value`` is a number, to be multiplied by the existing amount.
    * ``remove_uncertainty``: Remove (unscaled) uncertainty data, default is ``True``.

    Returns the modified exchange."""
    assert isinstance(exc, dict), "Must pass exchange dictionary"
    assert isinstance(value, Number), "Constant factor ``value`` must be a number"

    exc["amount"] *= value

    FIELDS = ("shape", "size", "minimum", "maximum")

    if remove_uncertainty:
        exc["uncertainty type"] = 0
        exc["loc"] = exc["amount"]
        for field in FIELDS:
            if field in exc:
                del exc[field]

    return exc
