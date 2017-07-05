Introduction
############

Wurst is a tool for merging or modifying life cycle inventory databases with other data sources. Current development focuses on modifying the ecoinvent LCI database with scenario data from various data sources, using Brightway2 as the data backend.

A wurst model run will typically consist of the following steps:

* Load data from several sources
* Modify the LCI data
* Write the modified LCI data to some storage mechanism

Wurst supports the following generic modification types:

* Change the input material efficiency and associated emissions
* Change specific emissions separate from general efficiency improvements
* Change the relative shares of inputs (including adding new inputs) into markets

In general, a modification function will include the following steps:

* Filter the LCI database by name, unit, location, etc. to get the subset of activities to modify
* Filter the external data source to get the relevant data used for modifications
* Change the values of some of the exchanges in the filtered LCI database

Searching and filtering
=======================

Wurst provides :ref:`helper functions <tech-searching>` to make searching and filtering easier. These functions are: ``equals``, ``contains``, ``startswith``, ``exclude``, ``either``. The filter functions are designed to be used with ``get_many`` and ``get_one``; here is an example:

.. code-block:: python

    nuclear_generation = get_many(
        lci_database,
        contains('name', 'nuclear'),
        contains('name', 'electricity'),
        equals('unit', 'kilowatt hour'),
        exclude(contains('name', 'aluminium')),
        exclude(contains('name', 'import'))
    )

It is also OK to write a generator function that does the same thing:

.. code-block:: python

    nuclear_generation = (
        ds for ds in lci_database
        if 'nuclear' in ds['name']
        and 'nuclear' in ds['name']
        and ds['unit'] == 'kilowatt hour'
        and 'aluminium' not in ds['name']
        and 'import' not in ds['name']
    )

The difference between the styles is ultimately a question of personal preference. For many people, list and generator expressions are more pythonic; in the specific case of wurst, using helper functions that are composable and reusable may allow you to not repeat yourself as often. There will also be times when the helper functions in wurst are not good enough for a specific search. In any case bear in mind the following general guidelines:

* Always manually check the results of your filtering functions before using them! The world is a complicated place, and our data sources reflect that complexity with unexpected or inconsistent elements.
* It is strongly recommended to use generator instead of list comprehensions, i.e. ``(x for x in foo)`` instead of ``[x for x in foo]``.

See also: `itertools <https://docs.python.org/3/library/itertools.html>`__, `functools <https://docs.python.org/3/library/functools.html>`__, `toolz <https://toolz.readthedocs.io/en/latest/index.html>`__.

Internal data format
====================

The internal data format for Wurst is a subset of the implied internal format for Brightway2.

.. code-block:: python

    {
        'database': str,
        'code': str,
        'name': str,
        'location': str,
        'unit': str,
        'classifications': [tuple],
        'comment': str,
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

