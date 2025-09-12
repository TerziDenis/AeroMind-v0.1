import g4f
from memory_manager import Memory

class ChatBot():
    def __init__(self):
        self.memory = Memory('../model_db.json')
        self.MODEL = "gpt-4"
        self.conversation_history = []
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self):
        return {
            'role': 'system',
            'content': (
                "Ты - интеллектуальный ассистент с доступом к внешней базе долговременной памяти. "
                "\n\n"
                "## ИНСТРУКЦИИ ПО РАБОТЕ С ПАМЯТЬЮ:\n"
                "1. ЕСЛИ пользователь просит ВСПОМНИТЬ какую-то информацию или которую ты знать не можешь "
                "(имя, предпочтения, данные, факты о себе и т.д.) →\n"
                "   → ВЕРНИ: \"MEMORY_READ: <ключ_на_английском>\"\n"
                "   Пример: \"MEMORY_READ: user_name\"\n\n"
                
                "2. ЕСЛИ пользователь просит ЗАПОМНИТЬ какую-либо информацию →\n"
                "   → ВЕРНИ ТОЛЬКО: \"MEMORY_WRITE: <ключ>=<значение>\"\n"
                "   Пример: \"MEMORY_WRITE: favorite_color=синий\"\n\n"
                
                "3. Ключи должны быть на английском, краткие и описательные:\n"
                "   - user_name, user_age, user_city\n"
                "   - favorite_color, favorite_food, favorite_movie\n"
                "   - phone_number, email_address, birth_date\n\n"
                
                "4. НИКОГДА не выдумывай данные\n"
                "5. Для всего остального отвечай как обычный ассистент\n\n"
                
                "Отвечай предельно кратко и по делу. Избегай лишних слов в ответах."
                "Всегда обращай внимание на инструкции с памятью"
            )
        }
    
    def get_reply(self, user_input):
        """Main get reply from AI method"""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        messages = [self.system_prompt] + self.conversation_history[-10:]  # Ограничиваем историю
        
        response = g4f.ChatCompletion.create(
            model=self.MODEL, 
            messages=messages,
            temperature=0.1,  
            max_tokens=500
        )
        
        # memory comands processing
        if response.startswith('MEMORY_READ:'):
            print(f"Промежуточный ответ {response}")
            final_reply = self._handle_memory_read(response, user_input)
        elif response.startswith('MEMORY_WRITE:'):
            print(f"Промежуточный ответ {response}")
            final_reply = self._handle_memory_write(response)
        else:
            final_reply = response
        
        self.conversation_history.append({"role": "assistant", "content": final_reply})
        
        return final_reply
    
    def _handle_memory_read(self, ai_reply, user_input):
        memory_key = ai_reply.replace("MEMORY_READ:", "").strip()
        stored_value, found_key = self.memory.read(memory_key)
        
        if stored_value:
            # Формируем контекстный запрос для ИИ
            context_message = {
                "role": "assistant",
                "content": f"Пользователь спросил: '{user_input}'. В памяти найдено: {stored_value}. Ответь естественно, используя эту информацию."
            }
            
            messages = [context_message]
            
            response = g4f.ChatCompletion.create(
                model=self.MODEL, 
                messages=messages,
                temperature=0.7
            )
            return response
        else:
            return f"Я не нашел информацию о '{memory_key}' в памяти. Может быть, вы хотите ее сохранить?"
    
    def _handle_memory_write(self, ai_reply):
        
        return self.memory.write(ai_reply)
    
    def test_connection(self):
        from termcolor import colored
        """AI connection test"""
        try:
            response = g4f.ChatCompletion.create(
                model=self.MODEL, 
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            if response:
                print(colored("✓ AI is connected and ready for work", 'green'))
                
                return True
            else:
                print(colored("✗ Servers is busy, try later", 'red'))
                
                return False
        except Exception as e:
            print(colored(f"✗ AI connection error: {e}", 'red'))
            
            return False
        
