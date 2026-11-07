import json
import os


class RatesStorage:
    """Класс для сохранения курсов в JSON-файл."""
    
    def save(self, filepath: str, data: dict):
        """Сохраняет данные в файл."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)