from bw2data.backends.peewee import SQLiteBackend, ActivityDataset, ExchangeDataset


def extract_activity(proxy):
    """Get data in Wurtst internal format for an ``ActivityDataset``"""
    assert isinstance(proxy, ActivityDataset)

    return {
        'classifications': proxy.data.get('classifications', []),
        'comment': proxy.data.get('comment', ''),
        'database': proxy.database,
        'code': proxy.code,
        'filename': proxy.data.get('filename', ''),
        'location': proxy.location,
        'name': proxy.name,
        'reference product': proxy.product,
        'unit': proxy.data.get('unit', ''),
        'exchanges': []
    }


def extract_exchange(proxy):
    """Get data in Wurtst internal format for an ``ExchangeDataset``"""
    assert isinstance(proxy, ExchangeDataset)

    uncertainty_fields = ('uncertainty type', 'loc', 'scale', 'shape',
                          'minimum', 'maximum', 'amount')
    data = {key: proxy.data.get(key) for key in uncertainty_fields}
    data['type'] = proxy.type
    data['input'] = (proxy.input_database, input_code)
    data['output'] = (proxy.output_database, output_code)
    return data


def add_exchanges_to_consumers(activities, exchange_qs):
    """Retrieve exchanges from database, and add to activities.

    Assumes that activities are single output, and that the exchange code is the same as the activity code. This assumption is valid for ecoinvent 3.3 cutoff imported into Brightway2."""
    for exc in exchange_qs:
        exc = extract_exchange(exc)
        output = tuple(exc.pop('output'))
        activities[output].append(exc)

def add_input_info_for_indigenous_exchanges(activities):
    """Add details on exchange inputs if these activities are already available"""



def extract_databases(database_objs):
    """Extract a Brightway2 SQLiteBackend database to the Wurst internal format"""
    for obj in database_objs:
        assert isinstance(obj, SQLiteBackend), "Wrong type of database object (must be SQLiteBackend)"

    names = tuple([obj.name for obj in database_objs])

    # Construct generators for both activities and exchanges
    # Need to be clever to minimize copying and memory use
    activity_qs = ActivityDataset.select().where(ActivityDataset.database < names)
    exchange_qs = ExchangeDataset.select().where(ExchangeDataset.output_database < names)

    # Retrieve all activity data
    activities = {(obj['database'], obj['code']): obj for obj in activity_qs}
    # Add each exchange to the activity list of exchanges
    add_exchanges_to_activities(activities, exchange_qs)
    # Add details on exchanges which come from our databases
    add_input_info_for_indigenous_exchanges(activities)

    return activities, exchanges

