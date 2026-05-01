class CurrencyStrategy:
    def __init__(self):
        self.rates = {
            "NGN": 1,
            "USD": 0.0007,
            "EUR": 0.0006,
            "GBP": 0.0005
        }

    def convert(self, amount, from_currency, to_currency):
        if from_currency not in self.rates or to_currency not in self.rates:
            print("Currency not supported")
            return

        base = amount / self.rates[from_currency]
        return base * self.rates[to_currency]


