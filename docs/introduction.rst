Introduction
############

Internal data format
====================

The internal data format for Wurst is a subset of the implied internal format for Brightway2.

.. code-block:: python

    {
        'classifications': [tuple],
        'comment': str,
        'location': str,
        'name': str,
        'reference product': str,
        'unit': str,
        'exchanges': [
            {
                'amount': float,
                'categories': list,  # only for biosphere flows
                'type': str,  # biosphere, techosphere, production
                'activity': str,
                'product': str,
                'unit': str,
                'location': str,
                'input': tuple,  # only if from external database
                'uncertainty type': int,   # optional
                'loc': float,              # optional
                'scale': float,            # optional
                'shape': float,            # optional
                'minimum': float,          # optional
                'maximum': float,          # optional
                'production volume': float # optional
                'pedigree': {              # optional
                    'completeness': int,
                    'further technological correlation': int,
                    'geographical correlation': int,
                    'reliability': int,
                    'temporal correlation': int
                },
            }
        ]
    }

An example classification:

.. code-block:: python

    ('ISIC rev.4 ecoinvent', '1050:Manufacture of dairy products')

