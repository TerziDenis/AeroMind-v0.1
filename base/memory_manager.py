import json
import re
import os
from typing import Dict, Optional

class Memory:
    def __init__(self, filename: str):
        self.filename = filename
        self.db = self._load_database()
    
    def _load_database(self) -> Dict[str, str]:
        """Загрузка базы данных из JSON файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except (FileNotFoundError, json.JSONDecodeError):
            # Создаем пустой файл с корректным JSON
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            return {}
    
    def _save_database(self) -> None:
        """Сохранение базы данных в файл"""
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def write(self, command: str) -> Dict[str, str]:
        """
        Запись данных в память
        Формат команды: MEMORY_WRITE: key=value
        """
        # Более гибкое регулярное выражение
        match = re.search(r"MEMORY_WRITE:\s*([^=]+?)\s*=\s*(.+)", command, re.IGNORECASE)
        if not match:
            raise ValueError("Ошибка формата команды. Используйте: MEMORY_WRITE: ключ=значение")
        
        key = match.group(1).strip().lower()
        value = match.group(2).strip()
        
        # Очистка значения от завершающих символов
        value = re.sub(r'[.,!?;]\s*$', '', value).strip()
        
        self.db[key] = value
        self._save_database()
        
        return self.db
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Получить значение по ключу"""
        return self.db.get(key.lower(), default)
    
    def get_all(self) -> Dict[str, str]:
        """Получить все сохраненные данные"""
        return self.db.copy()
    
    def delete(self, key: str) -> bool:
        """Удалить конкретное значение"""
        key = key.lower()
        if key in self.db:
            del self.db[key]
            self._save_database()
            print(f"✓ Удалено: {key}")
            return True
        return False
    
    def clear(self) -> None:
        """Очистить всю память"""
        self.db.clear()
        self._save_database()
        print("✓ Вся память очищена")
    
    def __contains__(self, key: str) -> bool:
        """Проверка наличия ключа"""
        return key.lower() in self.db
    
    def __getitem__(self, key: str) -> str:
        """Получение значения по ключу"""
        return self.db[key.lower()]
    
    def __setitem__(self, key: str, value: str) -> None:
        """Установка значения по ключу"""
        self.db[key.lower()] = value.strip()
        self._save_database()
                  