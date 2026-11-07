from datetime import datetime

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.logging_config import logger
from valutatrade_hub.parser_service.api_clients import CoinGeckoClient
from valutatrade_hub.parser_service.config import ParserConfig
from valutatrade_hub.parser_service.storage import RatesStorage


class RatesUpdater:
    """Главный класс парсера."""
    
    def __init__(self):
        self.client = CoinGeckoClient()
        self.storage = RatesStorage()
    
    def run_update(self):
        """Обновляет курсы и сохраняет их."""
        
        try:
            rates = self.client.fetch_rates()
            
            data = {
                "pairs": rates,
                "last_refresh": datetime.now().isoformat()
            }
            
            self.storage.save(ParserConfig.RATES_FILE_PATH, data)
            
            logger.info(f"Successfully updated {len(rates)} rates.")
            print(f"Update successful. Total rates updated: {len(rates)}")
            
        except (ApiRequestError, OSError, ValueError) as e:
            logger.error(f"Update failed: {e}")
            print(f"Error: {e}")