from abc import ABC, abstractmethod

from valutatrade_hub.core.exceptions import CurrencyNotFoundError


class Currency(ABC):
    """Абстрактный базовый класс."""
    
    def __init__(self, name: str, code: str):
        if not name:
            raise ValueError("Имя валюты не может быть пустым")
        self.name = name
        self.code = code
    
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value):
        value = value.upper()
        if not (2 <= len(value) <= 5):
            raise ValueError("Код валюты должен содержать от 2 до 5 символов")
        if " " in value:
            raise ValueError("Код валюты не может содержать пробелы")
        self._code = value

    @abstractmethod
    def get_display_info(self) -> str:
        """Возвращает строку для UI."""

class FiatCurrency(Currency):
    def __init__(self, name: str, code: str, issuing_country: str):
        super().__init__(name, code)
        self.issuing_country = issuing_country

    def get_display_info(self) -> str:
        return f'[FIAT] {self.code} — {self.name} (Issuing: {self.issuing_country})'


class CryptoCurrency(Currency):
    def __init__(self, name: str, code: str, algorithm: str, market_cap: float):
        super().__init__(name, code)
        self.algorithm = algorithm
        self.market_cap = market_cap

    def get_display_info(self) -> str:
        return f'[CRYPTO] {self.code} — {self.name} (Algo: {self.algorithm}, MCAP: {self.market_cap:.2e})'

_CURRENCIES = {
    "USD": FiatCurrency("US Dollar", "USD", "United States"),
    "EUR": FiatCurrency("Euro", "EUR", "Eurozone"),
    "GBP": FiatCurrency("British Pound", "GBP", "United Kingdom"),
    "RUB": FiatCurrency("Russian Ruble", "RUB", "Russia"),
    "JPY": FiatCurrency("Japanese Yen", "JPY", "Japan"),
    "BTC": CryptoCurrency("Bitcoin", "BTC", "SHA-256", 1.12e12),
    "ETH": CryptoCurrency("Ethereum", "ETH", "Ethash", 3.5e11),
    "SOL": CryptoCurrency("Solana", "SOL", "PoH", 6.5e10),
    "XRP": CryptoCurrency("Ripple", "XRP", "RPCA", 3.2e10),
    "ADA": CryptoCurrency("Cardano", "ADA", "Ouroboros", 1.5e10),
}

def get_currency(code: str) -> Currency:
    """Возвращает объект валюты по коду."""
    code = code.upper()
    if code not in _CURRENCIES:
        raise CurrencyNotFoundError(f"Неизвестная валюта '{code}'")
    return _CURRENCIES[code]