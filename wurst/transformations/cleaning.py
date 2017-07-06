def delete_zero_amount_exchanges(data, types=None):
    if types:
        dont_delete = lambda x: x['type'] not in types or x['amount']
    else:
        dont_delete = lambda x: x['amount']
    for ds in data:
        ds['exchanges'] = filter(dont_delete, ds['exchanges'])
    return data
