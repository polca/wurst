Internal data format
====================

To ease interaction with Brightway2, the internal format for Wurst is a subset of the implied internal format for Brightway2.

.. code-block:: python

    {
        'classifications': [tuple],
        'comment': str,
        'filename': str,
        'location': str,
        'name': str,
        'reference product': str,
        'unit': str,
        'exchanges': [
            {
                'input': {
                    'name': str,
                    'database': str,
                    'unit': str,
                    'location': str,
                },
                'type': str,  # biosphere, techosphere, production
                'name': str,
                'unit': str,
                'amount': float,
                'uncertainty type': int,  # optional
                'loc': float,             # optional
                'scale': float,           # optional
                'shape': float,           # optional
                'minimum': float,         # optional
                'maximum': float,         # optional
            }
        ]
    }
