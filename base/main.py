# Тут у нас запускается код, основной файл
# подтягиваем вначале обработку микрофона отдаём иишке и получаем ответ и печатаем
from dotenv import load_dotenv
from client import ChatBot
from voice_node import VoiceNode

import time
import os

load_dotenv()
def main():
    bot = ChatBot()
    voice = VoiceNode(['alexa'])
    
    test = bot.test_connection()
    if test:
        pass
    else:
        return
    
    while True:#Main work cycle
        try:
            user_input = voice.voice_hearing_start()# тут звук преобразовываем в текст
            if user_input:
                if user_input == 'выход':
                    break
                print(user_input)
                start_time = time.time()
                reply = bot.get_reply(user_input)# тут нейронка получает текст и сразу возвращает ответ
                end_time = time.time()
                
                print(f'Бот: {reply}')
                print(f'Время ответа: {end_time - start_time:.2f} сек')# контроль качества небольшой
            else:
                pass
        
        except KeyboardInterrupt:
            print("\nЗавершение работы...")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            break

if __name__ == "__main__":
    main()
    
