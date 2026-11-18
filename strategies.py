
class FixedSpreadStrategy:
    def __init__(self, spread=1.0):
        self.spread = spread

    def get_quotes(self, market_price, inventory):
        half_spread = self.spread / 2

        bid = market_price - half_spread
        ask = market_price + half_spread

        return bid, ask


class InventoryAwareStrategy:
    def __init__(self, spread=1.0, skew=0.05):
        self.spread = spread
        self.skew = skew

    def get_quotes(self, market_price, inventory):
        half_spread = self.spread / 2

        reservation_price = (
            market_price - self.skew * inventory
        )

        bid = reservation_price - half_spread
        ask = reservation_price + half_spread

        return bid, ask
