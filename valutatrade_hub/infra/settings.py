import tomllib


class SettingsLoader:
    """Единая точка настроек приложения (Singleton)."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            
            # 1. Сначала задаём значения по умолчанию
            cls._instance.data_dir = "data"
            cls._instance.rates_ttl = 300
            cls._instance.base_currency = "USD"
            cls._instance.log_file = "logs/actions.log"
            
            try:
                with open("pyproject.toml", "rb") as f:
                    config = tomllib.load(f)
                
                if "valutatrade" in config.get("tool", {}):
                    vt = config["tool"]["valutatrade"]
                    cls._instance.data_dir = vt.get("data_dir", "data")
                    cls._instance.rates_ttl = vt.get("rates_ttl_seconds", 300)
                    cls._instance.base_currency = vt.get("default_base_currency", "USD")
                    cls._instance.log_file = vt.get("log_file", "logs/actions.log")
            except FileNotFoundError:
                pass  
        
        return cls._instance
    
    def get(self, key, default=None):
        return getattr(self, key, default)