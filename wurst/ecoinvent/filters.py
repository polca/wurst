from ..searching import *

coal_electricity = [
    either(contains('name', 'hard coal'), contains('name', 'lignite')),
    contains('name', 'electricity'),  # Do we need this?
    equals('unit', 'kilowatt hour'),
]
