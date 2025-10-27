from numbers import Number
import math


def rescale_exchange(exc, value, remove_uncertainty=True):
    """Function to rescale exchange amount and uncertainty.

    * ``exc`` is an exchange dataset.
    * ``value`` is a number, to be multiplied by the existing amount.
    * ``remove_uncertainty``: Remove (unscaled) uncertainty data, default is ``True``.
    If ``False``, uncertainty data is scaled by the same factor as the amount
    (except for lognormal distributions, where the ``loc`` parameter is scaled by the log of the factor).
    Currently, does not rescale for Bernoulli, Discrete uniform, Weibull, Gamma, Beta, Generalized Extreme value
    and Student T distributions.

    Returns the modified exchange."""
    assert isinstance(exc, dict), "Must pass exchange dictionary"
    assert isinstance(value, Number), "Constant factor ``value`` must be a number"

    # Scale the amount
    exc["amount"] *= value

    # Scale the uncertainty fields if uncertainty is not being removed
    if not remove_uncertainty and "uncertainty type" in exc:
        uncertainty_type = exc["uncertainty type"]

        # No uncertainty, do nothing
        if uncertainty_type in {0, 6, 7, 8, 9, 10, 11, 12}:
            pass
        elif uncertainty_type in {1, 2, 3, 4, 5}:
            # Scale "loc" by the log of value for lognormal distribution
            if "loc" in exc and uncertainty_type == 2:
                exc["loc"] += math.log(value)
            elif "loc" in exc:
                exc["loc"] *= value

            # "scale" stays the same for lognormal
            # For other distributions, scale "scale" by the absolute value
            if "scale" in exc and uncertainty_type not in {2}:
                exc["scale"] *= abs(value)

            # Scale "minimum" and "maximum" by value
            for bound in ("minimum", "maximum"):
                if bound in exc:
                    exc[bound] *= value

    # If remove_uncertainty is True, then remove all uncertainty info
    elif remove_uncertainty:
        FIELDS = ("scale", "minimum", "maximum", )
        exc["uncertainty type"] = 0
        exc["loc"] = exc["amount"]
        for field in FIELDS:
            if field in exc:
                del exc[field]

    return exc
