.. _technical:

Technical Reference
===================

.. _tech-searching:

Searching
---------

.. autofunction:: wurst.searching.equals

.. autofunction:: wurst.searching.contains

.. autofunction:: wurst.searching.startswith

.. autofunction:: wurst.searching.either

.. autofunction:: wurst.searching.exclude

.. autofunction:: wurst.searching.doesnt_contain_any

.. autofunction:: wurst.searching.get_many

.. autofunction:: wurst.searching.get_one

Exchange iterators
------------------

.. autofunction:: wurst.searching.technosphere

.. autofunction:: wurst.searching.biosphere

.. autofunction:: wurst.searching.production

.. autofunction:: wurst.searching.reference_product

Geo functions
-------------

.. autofunction:: wurst.ecoinvent.get_ordered_geo_relationships

.. autofunction:: wurst.searching.best_geo_match

Linking
-------

.. autofunction:: wurst.linking.link_internal

.. autofunction:: wurst.linking.check_internal_linking

.. autofunction:: wurst.linking.change_db_name

.. autofunction:: wurst.linking.check_duplicate_codes

Transformations
---------------

.. autofunction:: wurst.transformations.activity.change_exchanges_by_constant_factor

.. autofunction:: wurst.transformations.copy_to_new_location

.. autofunction:: wurst.transformations.relink_technosphere_exchanges

.. autofunction:: wurst.transformations.delete_zero_amount_exchanges

.. autofunction:: wurst.transformations.rescale_exchange

.. autofunction:: wurst.transformations.default_global_location

.. autofunction:: wurst.transformations.empty_market_dataset

Brightway2 IO
-------------

.. autofunction:: wurst.brightway.extract_database.extract_brightway2_databases

.. autofunction:: wurst.brightway.write_database.write_brightway2_database

