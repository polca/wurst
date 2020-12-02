class MultipleResults(Exception):
    """Multiple results returned when only one is desired"""

    pass


class NoResults(Exception):
    """No results found when some were expected"""

    pass


class InvalidLink(Exception):
    """Exchange link is to a missing activity"""

    pass


class NonuniqueCode(Exception):
    """Codes should be unique, but these aren't"""

    pass
