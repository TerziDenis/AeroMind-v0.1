from dotenv import load_dotenv

import pvporcupine
import os
import pyaudio
import struct


class Detector():
    """
    Keyword detector class, 
    """
    def __init__(self, keywords: list):
        load_dotenv()
        self.ACCESS_KEY = os.getenv('PICOVOICE_ACCESS_KEY')
        self.handler =  pvporcupine.create(access_key=self.ACCESS_KEY, keywords=keywords)

        self.SAMPLE_RATE = self.handler.sample_rate
        self.FRAME_LENGTH = self.handler.frame_length  # 512 семплов
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paInt16
        self.mic_stream_start()

    def mic_stream_start(self):
        self.audio = pyaudio.PyAudio()

        # Создаем аудиопоток - буфер должен быть в 2 раза больше!
        stream = self.audio.open(
            rate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            format=self.FORMAT,
            input=True,
            frames_per_buffer=self.FRAME_LENGTH  # 512 семплов
        )
        
        return stream

    def detection(self, stream): 
        while True:
            # Читаем данные из микрофона (получаем 1024 байта)
            data = stream.read(self.FRAME_LENGTH, exception_on_overflow=False)
            #Преобразуем байты в семплы
            pcm_data = struct.unpack_from("h" * self.FRAME_LENGTH, data)
            
            # Передаем правильно сформированные данные в Porcupine
            keyword_index = self.handler.process(pcm_data)
            
            if keyword_index >= 0:
                # Точка выхода из функции, ключевое слово было услышано
                
                return -1

         
        
       