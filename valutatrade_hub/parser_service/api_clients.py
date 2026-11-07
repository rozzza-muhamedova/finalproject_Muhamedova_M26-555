from abc import ABC, abstractmethod

import requests

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.parser_service.config import ParserConfig


class BaseApiClient(ABC):
    """Базовый класс для всех API-клиентов."""
    
    @abstractmethod
    def fetch_rates(self) -> dict:
        pass


class CoinGeckoClient(BaseApiClient):
    """Клиент для получения курсов с CoinGecko."""
    
    def fetch_rates(self) -> dict:
        """Стучится в API CoinGecko и возвращает словарь {'BTC_USD': 59337.21, ...}."""
        
        ids = ",".join(ParserConfig.CRYPTO_ID_MAP.values())
        params = {
            "ids": ids,
            "vs_currencies": ParserConfig.BASE_CURRENCY.lower(),  # Должно быть .lower()
        }
        
        try:
            response = requests.get(
                ParserConfig.COINGECKO_URL,
                params=params,
                timeout=ParserConfig.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            rates = {}
            for ticker, coin_id in ParserConfig.CRYPTO_ID_MAP.items():
                # Тут ОБЯЗАТЕЛЬНО должен быть .lower()
                if coin_id in data and ParserConfig.BASE_CURRENCY.lower() in data[coin_id]:
                    rate = data[coin_id][ParserConfig.BASE_CURRENCY.lower()]
                    pair = f"{ticker}_{ParserConfig.BASE_CURRENCY.upper()}"
                    rates[pair] = rate
                    
            return rates
            
        except requests.RequestException as e:
            raise ApiRequestError(f"Ошибка при запросе к CoinGecko: {e}")