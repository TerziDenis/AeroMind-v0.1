import json
import re
import os

from typing import Tuple, Any, Optional


class Memory:
    def __init__(self, filename: str):
        self.filename = filename
        self.db = self._load_database()
    
    def _load_database(self) -> dict:
        """Загрузка базы данных из JSON файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filename, 'w') as f:
                f.write('{}')
            return self._load_database()
    
    def _save_database(self):
        """Сохранение базы данных в файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def write(self, command: str) -> str:
        """
        Запись данных в память
        Формат команды: MEMORY_WRITE: key=value
        """
        match = re.match(r"MEMORY_WRITE:\s*([^=]+?)\s*=\s*(.+)", command, re.IGNORECASE)
        if not match:
            return "Ошибка формата команды записи. Используйте: MEMORY_WRITE: ключ=значение"
        
        key = match.group(1).strip().lower()
        value = match.group(2).strip()
        
        # Очистка значения от лишних символов
        value = re.split(r'[.,!?;]', value)[0].strip()
        
        self.db[key] = value
        self._save_database()
        
        return f"✓ Сохранено в память: {key} = {value}"
    
    def read(self, search_query: str) -> Tuple[Optional[Any], str]:
        """
        Поиск данных в памяти
        Возвращает (значение, найденный_ключ)
        """
        clean_query = search_query.replace("MEMORY_READ:", "").strip().lower()
        
        # Прямой поиск по ключу
        if clean_query in self.db:
            return self.db[clean_query], clean_query
        
        # Поиск по частичному совпадению ключей
        for key in self.db.keys():
            if clean_query in key.lower():
                return self.db[key], key
        
        # Поиск по значениям
        for key, value in self.db.items():
            if isinstance(value, str) and clean_query in value.lower():
                return value, key
        
        return None, clean_query
    
    def get_all_memories(self) -> dict:
        """Получить все сохраненные воспоминания"""
        return self.db.copy()
    
    def clear_memory(self, key: str = None) -> str:
        """Очистить конкретное воспоминание или всю память"""
        if key:
            if key in self.db:
                del self.db[key]
                self._save_database()
                return f"✓ Удалено: {key}"
            else:
                return f"✗ Ключ '{key}' не найден"
        else:
            self.db.clear()
            self._save_database()
            return "✓ Вся память очищена"
                  