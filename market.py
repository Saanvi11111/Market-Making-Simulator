
import numpy as np


def generate_market(
    n_steps=1000,
    start_price=100.0,
    volatility=0.5,
    seed=None
):
    rng = np.random.default_rng(seed)

    price_changes = rng.normal(0, volatility, n_steps)
    prices = start_price + np.cumsum(price_changes)

    order_sides = rng.choice(
        ["buy", "sell"],
        size=n_steps
    )

    order_sizes = rng.integers(1, 6, size=n_steps)

    market = []

    for i in range(n_steps):
        market.append({
            "price": prices[i],
            "side": order_sides[i],
            "size": order_sizes[i]
        })

    return market
