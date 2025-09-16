import g4f

from memory_manager import Memory
from modules import color_print

class ChatBot():
    def __init__(self):
        self.memory_manager = Memory('../model_db.json')
        self.memory = self.memory_manager.db
        self.MODEL = "gpt-4"
        self.conversation_history = []
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self):
        current_memory = self.memory_manager.get_all()
        memory_str = "\n".join([f"{key}: {value}" for key, value in current_memory.items()])
        
        return {
            'role': 'system',
            'content': (
                "Ты - AI ассистент с долговременной памятью.\n\n"
                f"ТЕКУЩАЯ ПАМЯТЬ:\n{memory_str}\n\n"
                "## ПРАВИЛА РАБОТЫ С ПАМЯТЬЮ:\n"
                "1. Всегда используй информацию из памяти при ответах\n"
                "2. Если пользователь просит ЗАПОМНИТЬ информацию →\n"
                "   → ОТВЕТЬ: \"MEMORY_WRITE: <ключ>=<значение>\"\n"
                "   Пример: \"MEMORY_WRITE: favorite_color=синий\"\n"
                "3. Используй английские ключи (user_name, favorite_color, etc.)\n\n"
                "Отвечай кратко и по делу. Без лишних слов."
            )
        }
    
    def get_reply(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        self.system_prompt = self._create_system_prompt()
        
        messages = [self.system_prompt] + self.conversation_history[-10:]
        
        response = g4f.ChatCompletion.create(
            model=self.MODEL, 
            messages=messages,
            temperature=0.1,  
            max_tokens=500
        )
        
        # Только обработка записи, чтение не нужно - память уже в контексте
        final_reply = self._process_response(response)
        self.conversation_history.append({"role": "assistant", "content": final_reply})
        
        return final_reply
    
    def _process_response(self, response: str) -> str:
        if response.startswith('MEMORY_WRITE:'):
            print(f"Промежуточный ответ: {response}")
            try:
                self.memory = self.memory_manager.write(response)
                
                return f"✓ Запомнил: {response.replace('MEMORY_WRITE:', '').strip()}"
            
            except Exception as e:
                
                return f"✗ Ошибка записи: {e}"
        else:
            
            return response
    
    def test_connection(self):
        try:
            response = g4f.ChatCompletion.create(
                model=self.MODEL, 
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            if response:
                color_print("✓ AI подключен", 'green')
                
                return True
            else:
                color_print("✗ Серверы перегружены", 'red')
                
                return False
       
        except Exception as e:
            color_print(f"✗ Ошибка подключения: {e}", 'red')
            
            return False
    
    def clear_memory(self, key: str = None) -> str:
        if key:
            success = self.memory_manager.delete(key)
            if success:
                self.memory = self.memory_manager.db
                
                return f"✓ Удалено: {key}"
            
            return f"✗ Ключ '{key}' не найден"
        else:
            self.memory_manager.clear()
            self.memory = self.memory_manager.db
            
            return "✓ Вся память очищена"
    
    def get_memory(self) -> dict:
        
        return self.memory_manager.get_all().copy()