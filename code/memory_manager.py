import json
import re


class Memory():
    def __init__(self, filename):
        self.filename = filename
        self.db_dict = self.load_json()
        
    def load_json(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = f.read().strip()
                if not data:  # если файл пустой
                    return {}
                return json.loads(data)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_json(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.db_dict, f, ensure_ascii=False, indent=2)
    
    def write(self, reply):
        match = re.match(r"MEMORY_WRITE:(.+?)=(.+)", reply)
        if match:
            key, value = match.group(1).strip(), match.group(2).strip()

            # ✂️ Обрезаем по первому знаку препинания
            cut_value = re.split(r'[.,!?]', value, 1)[0].strip()

            self.db_dict[key] = cut_value
            self.save_json()
            return f"Запомнил: {key} = {cut_value}"

    def read(self, reply):
        query = reply.replace("MEMORY_READ:", "").strip()

        # ⚡ быстрый поиск по ключу
        if query in self.db_dict:
            context = self.db_dict[query]
        else:
            # запасной вариант: поиск по значениям
            context = None
            for key, value in self.db_dict.items():
                if query.lower() in str(value).lower():
                    context = value
                    break
        
        return context, query
                  