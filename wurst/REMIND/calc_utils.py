from .metadata import REGIONS


def relative_change(dataset, years, start, end):
    """Calculate fractional change values from year ``start`` to year ``end``.

    Assumes years are the last axis of the array. Normalizes by the starting value."""
    years = list(years)
    return (
        dataset[..., years.index(end)] - dataset[..., years.index(start)]
    ) / dataset[..., years.index(start)]


def convert_to_location_dictionary(array, locations=REGIONS):
    """Convert array of values ``array`` with order ``locations`` to a dictionary:

        {
            'place name': value
        }

    Assumes that the first axis of the array matches the locations."""
    size = array.shape[0]
    if len(array.shape) == 1:
        return {
            loc: array[index] for index, loc in enumerate(locations) if index < size
        }
    else:
        return {
            loc: array[index, ...]
            for index, loc in enumerate(locations)
            if index < size
        }
