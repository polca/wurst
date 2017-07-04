class MultipleResults(Exception):
    """Multiple results returned when only one is desired"""
    pass


class NoResults(Exception):
    """No results found when some were expected"""
    pass
