from openai import OpenAI
from memory_manager import Memory


class Client(OpenAI):
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.memory = Memory('../model_db.json')
        self.conversation = [{
            'role': 'system',
            'content': (
                "Ты умный ассистент с доступом к внешней базе памяти. "
                "Если пользователь спрашивает что-то, что ты не можешь знать сам или просит вспомнить что-то"
                "(например, его имя, пароли, любимые вещи, персональные факты и т.д.), "
                "то вместо ответа нужно вернуть: "
                "\"MEMORY_READ: <ключевое_слово_на_английском>\". "
                "Ключевое слово должно быть кратким и отражать суть информации "
                "(например user_name, favorite_color, password). "
                "\n\n"
                "Если пользователь просит запомнить какую-то информацию, "
                "то верни только: "
                "\"MEMORY_WRITE: <ключ>=<значение>\". "
                "Например: MEMORY_WRITE: user_name=Denis. и больше ничего"
                "\n\n"
                "Ты НЕ должен выдумывать данные из памяти — если нужной информации нет, "
                "используй MEMORY_READ. "
                "Ты НЕ должен хранить память сам — только отдавай инструкции "
                "MEMORY_READ / MEMORY_WRITE. "
                "\n\n"
                "Отвечай кратко и по делу."
                "Если пользователь не просит что-то вспомнить или записать, отвечай как обычно"
            )
        }]
        self.MODEL = "deepseek-chat"
    
    def model_test(self):
        reply = self.chat.completions.create(model=self.MODEL, messages='Hello')
        if reply:
            pass
        else:
            raise Exception("AI not ready for work")
    
    def memory_read(self, reply, user_input):
        context, query = self.memory.read(reply)
            
        if context:
            # Вместо MEMORY_READ пишем в разговор готовый контекст
            self.conversation.append({
                "role": "system", 
                "content":  
                            f"{user_input}, Ответ на вопрос пользователя:{context}. "
                            f"Сформулируй для пользователя человеческий ответ,"
                            f"используя эти данные."
            })
            reply = self.chat.completions.create(model=self.MODEL, messages=self.conversation)
            return reply
        else:
            return f"В памяти ничего не найдено по запросу: {query}"


    def memory_write(self, reply):
        return self.memory.write(reply)
    
    def get_reply(self, query):
        self.conversation.append({"role": "user", "content": query})
        reply: str = self.chat.completions.create(model=self.MODEL, messages=self.conversation)

        if reply.startswith('MEMORY_READ'):
            reply = self.memory_read(reply, query)
        elif reply.startswith('MEMORY_WRITE'):
            reply = self.memory_write(reply)
        
        self.conversation.append({"role": "assistant", "content": reply})    
    
        return reply
        
