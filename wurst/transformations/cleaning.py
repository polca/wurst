def delete_zero_amount_production_exchanges(data):
    dont_delete = lambda x: x['type'] != 'production' or x['amount']
    for ds in data:
        ds['exchanges'] = filter(dont_delete, ds['exchanges'])
    return data
