from client import Client

import multiprocessing
import time

bot = Client(api_key='sk-a8bb95eca52448d4b504931f3e5fbfb4', base_url='https://api.deepseek.com')

while True:
    user_input = input('>>>')

    start_time = time.time()

    reply = bot.get_reply(user_input)
    
