
import numpy as np


def run_session(
    strategy,
    market,
    position_limit=50,
    execution_sensitivity=1.5,
    seed=None
):
    rng = np.random.default_rng(seed)

    cash = 0.0
    inventory = 0

    pnl_history = []
    inventory_history = []

    for event in market:
        price = event["price"]
        side = event["side"]
        size = event["size"]

        bid, ask = strategy.get_quotes(price, inventory)

        if side == "buy":
            fill_probability = np.exp(
                -execution_sensitivity * (ask - price)
            )
            fill_probability = min(1.0, max(0.0, fill_probability))

            if inventory > -position_limit:
                if rng.random() < fill_probability:
                    quantity = min(size, inventory + position_limit)
                    cash += ask * quantity
                    inventory -= quantity

        else:
            fill_probability = np.exp(
                -execution_sensitivity * (price - bid)
            )
            fill_probability = min(1.0, max(0.0, fill_probability))

            if inventory < position_limit:
                if rng.random() < fill_probability:
                    quantity = min(size, position_limit - inventory)
                    cash -= bid * quantity
                    inventory += quantity

        pnl = cash + inventory * price

        pnl_history.append(pnl)
        inventory_history.append(inventory)

    return {
        "pnl_history": pnl_history,
        "inventory_history": inventory_history,
        "final_pnl": pnl_history[-1],
        "max_inventory": max(abs(x) for x in inventory_history),
        "average_inventory": np.mean(
            [abs(x) for x in inventory_history]
        )
    }
