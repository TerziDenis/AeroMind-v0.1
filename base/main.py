import time
import os

from dotenv import load_dotenv
from client import ChatBot
from voice_node import VoiceNode


load_dotenv()#Loading .env file

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
            user_request = voice.voice_hearing_start()# Voice to text
            if user_request:
                if user_request == any(['exit', 'выход']):
                    break
                print(user_request)
                start_time = time.time()
                ai_reply = bot.get_reply(user_request)# Ai gets request and returns response
                end_time = time.time()
                
                print(f'Bot: {ai_reply}')
                print(f'Response time: {end_time - start_time:.2f} secs')# a lil bit of quality control :)
            else:
                pass
        
        except KeyboardInterrupt:
            print("\nTurning off...")
            
            break
        except Exception as e:
            print(f"Error: {e}")
            
            break

if __name__ == "__main__":
    main()
    
