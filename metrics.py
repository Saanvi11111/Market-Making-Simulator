
import numpy as np


def calculate_metrics(results):
    final_pnls = [r["final_pnl"] for r in results]

    average_inventory = np.mean([
        r["average_inventory"] for r in results
    ])

    worst_session_pnl = min(final_pnls)

    worst_case_loss = max(0, -worst_session_pnl)

    session_drawdowns = []

    for result in results:
        pnl_history = [0] + result["pnl_history"]

        peak = pnl_history[0]
        max_drawdown = 0

        for pnl in pnl_history:
            peak = max(peak, pnl)
            drawdown = peak - pnl
            max_drawdown = max(max_drawdown, drawdown)

        session_drawdowns.append(max_drawdown)

    losing_sessions = sum(
        1 for pnl in final_pnls if pnl < 0
    )

    return {
        "average_pnl": np.mean(final_pnls),
        "average_inventory": average_inventory,
        "worst_session_pnl": worst_session_pnl,
        "worst_case_loss": worst_case_loss,
        "max_inventory": max(
            r["max_inventory"] for r in results
        ),
        "worst_max_drawdown": max(session_drawdowns),
        "average_max_drawdown": np.mean(session_drawdowns),
        "losing_sessions": losing_sessions,
        "winning_sessions": len(results) - losing_sessions
    }


def percentage_reduction(old_value, new_value):
    if old_value == 0:
        return 0.0

    return ((old_value - new_value) / old_value) * 100
