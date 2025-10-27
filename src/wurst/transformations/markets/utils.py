def market_like(ds):
    """Find market activities which aren't called markets.

    Check to see if there are inputs with the same product as the reference product which sum to between the production amount and the production amount * 1.5."""
    rp = ds["reference product"]
    similar_inputs = (
        exc
        for exc in ds["exchanges"]
        if exc["type"] == "technosphere" and exc["product"] == rp
    )
    amount = [exc for exc in ds["exchanges"] if exc["type"] == "production"][0][
        "amount"
    ]
    return amount <= sum(exc["amount"] for exc in similar_inputs) <= amount * 1.5


def ecoinvent_market(ds):
    return (
        ds["name"].startswith("market for")
        or ds["name"].startswith("market group")
        # or market_like(ds)
    )
