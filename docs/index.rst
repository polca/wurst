Introduction
############

Show how the sausage is made!

Wurst is a python package for linking and modifying industrial ecology models, with a focus on sparse matrices in life cycle assessment. Current development focuses on modifying the ecoinvent LCI database with scenario data from various data sources, using Brightway2 as the data backend.

See an `example notebook <https://github.com/cmutel/wurst/blob/master/docs/notebooks/marginal-mixes.ipynb>`__ to see a typical use case for wurst.

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
* Change the values of some of the exchanges in the filtered LCI database using the filtered external data

Documents versus matrices
=========================

Inventory matrices can be modified by multiplying or adding vectors, as in the [Themis methodology paper](http://pubs.acs.org/doi/abs/10.1021/acs.est.5b01558). Wurst takes a different approach - it treats each activity (column in the technosphere matrix) as a document with metadata and a list of exchanges which can be modified as desired. This approach allows for both flexibility (e.g. the number of rows and columns are not fixed) and simpler code (no need for an indirection layer to row and column indices). So, instead of constructing a vector and using it directly, wurst would prefer to write a function like:

.. code-block:: python

    import wurst as w

    def scale_biosphere_exchanges_by_delta(ds, delta):
        # Not directly related to fuel inputs
        exclude_list = [
            'Methane, fossil', 'Sulfur dioxide',
            'Carbon monoxide, fossil',
            'Nitrogen oxides', 'Dinitrogen monoxide', 'Particulates'
        ]
        for exc in w.biosphere(ds, w.doesnt_contain_any('name', exclude_list)):
            # Modifies in place
            w.rescale_exchage(exc, delta)

Internal data format
--------------------

The internal data format for Wurst is a subset of the implied internal format for Brightway2.

.. code-block:: python

    {
        'database': str,
        'code': str,
        'name': str,
        'reference product': str,
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

Searching and filtering
=======================

Wurst provides :ref:`helper functions <tech-searching>` to make searching and filtering easier. These filter functions are designed to be used with ``get_many`` and ``get_one``; here is an example:

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

See the :ref:`API documentation for searching <tech-searching>`, and: `itertools <https://docs.python.org/3/library/itertools.html>`__, `functools <https://docs.python.org/3/library/functools.html>`__, `toolz <https://toolz.readthedocs.io/en/latest/index.html>`__.

Exchange iterators
------------------

Re-linking
==========

Built-in models
===============

.. toctree::
   :maxdepth: 1

   marginals

Technical documentation
=======================

.. toctree::
   :maxdepth: 1

   technical

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
