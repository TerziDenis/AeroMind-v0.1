from ww_detector import Detector
from stt import SpeechRecorder

class VoiceNode():
    def __init__(self, keywords: list):
        self.detector = Detector(keywords)
        self.stt = SpeechRecorder()
        self.voice_stream = self.detector.mic_stream_start()

    def voice_hearing_start(self):
        """
        Initiates keyword detetcor, start records voice and translating it to text, returns it
        """
        
        print("Слушаю кодовое слово")
        
        result = self.detector.detection(self.voice_stream)#слушаем ключевое слово

        if(result == -1):# ключевое слово услышано
            #Сюда поставлю звуковой сигнал который укажет на то что комп слышит и начал запись
            text = self.stt.record_and_recognize()#тут получаем текст из звука
            
        return text

