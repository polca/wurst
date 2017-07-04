def market_like(ds):
    pass


def ecoinvent_market(ds):
    return (
        ds['name'].startswith("market for") or
        ds['name'].startswith("market group") or
        market_like(ds)
    )
