
import matplotlib.pyplot as plt

from market import generate_market
from strategies import (
    FixedSpreadStrategy,
    InventoryAwareStrategy
)
from simulator import run_session
from metrics import (
    calculate_metrics,
    percentage_reduction
)


def main():
    num_sessions = 100
    num_steps = 1000

    fixed_results = []
    inventory_results = []

    example_fixed = None
    example_inventory = None

    fixed_strategy = FixedSpreadStrategy(spread=1.0)

    inventory_strategy = InventoryAwareStrategy(
        spread=1.0,
        skew=0.05
    )

    for session in range(num_sessions):

        market = generate_market(
            n_steps=num_steps,
            start_price=100.0,
            volatility=0.5,
            seed=session
        )

        fixed_result = run_session(
            fixed_strategy,
            market,
            position_limit=50,
            seed=10000 + session
        )

        inventory_result = run_session(
            inventory_strategy,
            market,
            position_limit=50,
            seed=10000 + session
        )

        fixed_results.append(fixed_result)
        inventory_results.append(inventory_result)

        if session == 0:
            example_fixed = fixed_result
            example_inventory = inventory_result

    fixed_metrics = calculate_metrics(fixed_results)
    inventory_metrics = calculate_metrics(inventory_results)

    print("\n=== MARKET-MAKING SIMULATOR ===")
    print(f"Sessions simulated: {num_sessions}")
    print(f"Steps per session: {num_steps}")

    print("\n=== FIXED SPREAD STRATEGY ===")

    for name, value in fixed_metrics.items():
        print(f"{name}: {value:.2f}")

    print("\n=== INVENTORY-AWARE STRATEGY ===")

    for name, value in inventory_metrics.items():
        print(f"{name}: {value:.2f}")

    print("\n=== STRATEGY COMPARISON ===")

    inventory_reduction = percentage_reduction(
        fixed_metrics["average_inventory"],
        inventory_metrics["average_inventory"]
    )

    loss_reduction = percentage_reduction(
        fixed_metrics["worst_case_loss"],
        inventory_metrics["worst_case_loss"]
    )

    print(
        f"Average inventory reduction: "
        f"{inventory_reduction:.2f}%"
    )

    print(
        f"Worst-case loss reduction: "
        f"{loss_reduction:.2f}%"
    )

    fig, axes = plt.subplots(2, 1, figsize=(11, 8))

    axes[0].plot(
        example_fixed["pnl_history"],
        label="Fixed Spread"
    )

    axes[0].plot(
        example_inventory["pnl_history"],
        label="Inventory Aware"
    )

    axes[0].set_title("Profit and Loss Over One Session")
    axes[0].set_xlabel("Time Step")
    axes[0].set_ylabel("P&L ($)")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(
        example_fixed["inventory_history"],
        label="Fixed Spread"
    )

    axes[1].plot(
        example_inventory["inventory_history"],
        label="Inventory Aware"
    )

    axes[1].set_title("Inventory Over One Session")
    axes[1].set_xlabel("Time Step")
    axes[1].set_ylabel("Shares Held")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig("strategy_comparison.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
