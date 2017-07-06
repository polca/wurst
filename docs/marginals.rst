.. _marginals:

Marginal electricity mixes
==========================

This model is based on the work of Laurent Vandepaer, and changes the electricity mixes (``market for electricity, low/medium/high voltage``) in the consequential version of ecoinvent. Input data is gathered from a number of different sources, and processed to an excel sheet that lists the absolute generation values for a number of ecoinvent electricity generators. This model is illustrated in the notebook `marginal-mixes.ipynb`.

This model needs to do the following:

* Import the input data
* Load ecoinvent, consequential system model
* Remove generators that aren't in current version of ecoinvent
* Normalize production values to sum to one kilowatt hour
* Remove all generators from low voltage production mix, replace complete with ``electricity voltage transformation from medium to low voltage``
* Remove all generators from medium voltage production mix, replace complete with ``electricity voltage transformation from high to medium voltage``
* Remove all generators from high voltage production mix, replace with new exchanges linked to our new generation technologies and amounts
* Relink all exchanges in the extracted database
* Write the database

Note that we move solar production from the low voltage mix to the high voltage mix, as new solar PV can be a large fraction of the marginal increase in production, more than 50% in some countries, but if it was stuck in the low voltage mix it would only be consumed by a few activities. Most activities consume electricity from the high voltage production mix.

The step removing some potential production technologies is needed because we are developing against ecoinvent 3.3, but our external import data is also linked against some technologies that will be included in 3.4. We skip these for now.

When we insert new production exchanges, we need to use a geo-matching function that finds the appropriate generation technology. Sometimes there are country-specific generators, but other times we will need to use a regional or even global producer.
