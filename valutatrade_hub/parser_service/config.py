from typing import ClassVar


class ParserConfig:
    """Конфигурация для сервиса парсинга."""
    
    # Эндпоинты
    COINGECKO_URL: str = "https://api.coingecko.com/api/v3/simple/price"
    
    # Списки валют
    BASE_CURRENCY: str = "USD"
    CRYPTO_CURRENCIES: tuple = ("BTC", "ETH", "SOL")
    CRYPTO_ID_MAP: ClassVar[dict] = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
    }
    
    # Пути
    RATES_FILE_PATH: str = "data/rates.json"
    HISTORY_FILE_PATH: str = "data/exchange_rates.json"
    
    REQUEST_TIMEOUT: int = 10