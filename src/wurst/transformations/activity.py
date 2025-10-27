from ..searching import technosphere, biosphere
from .uncertainty import rescale_exchange
from numbers import Number
import logging


logger = logging.getLogger("wurst")


def change_exchanges_by_constant_factor(
    ds, value, technosphere_filters=None, biosphere_filters=None
):
    """Change some or all inputs and biosphere flows by a constant factor.

    * ``ds`` is a dataset document.
    * ``value`` is a number. Existing exchange amounts will be multiplied by this number.
    * ``technosphere_filters`` is an iterable of filter functions. Optional.
    * ``biosphere_filters`` is an iterable of filter functions. Optional.

    Returns the altered dataset. The dataset is also modified in place, so the return value can be ignored.

    Example: Changing coal dataset to reflect increased fuel efficiency

    .. code-block:: python

        import wurst as w

        apct_products = w.either(
            w.equals('name', 'market for NOx retained'),
            w.equals('name', 'market for SOx retained'),
        )

        generation_filters = [
            w.either(w.contains('name', 'coal'), w.contains('name', 'lignite')),
            w.contains('name', 'electricity'),
            w.equals('unit', 'kilowatt hour'),
            w.doesnt_contain_any('name', [
                'market', 'aluminium industry',
                'coal, carbon capture and storage'
            ])
        ]

        fuel_independent = w.doesnt_contain_any('name', (
            'Methane, fossil', 'Sulfur dioxide', 'Carbon monoxide, fossil',
            'Nitrogen oxides', 'Dinitrogen monoxide', 'Particulates'
        ))

        for ds in w.get_many(data, generation_filters):
            change_exchanges_by_constant_factor(
                ds,
                0.8,  # Or whatever from input data
                [w.exclude(apct_products)],
                [fuel_independent]
            )

    """
    assert isinstance(ds, dict), "Must pass dataset dictionary document"
    assert isinstance(value, Number), "Constant factor ``value`` must be a number"

    for exc in technosphere(ds, *(technosphere_filters or [])):
        rescale_exchange(exc, value)
    for exc in biosphere(ds, *(biosphere_filters or [])):
        rescale_exchange(exc, value)

    return ds
