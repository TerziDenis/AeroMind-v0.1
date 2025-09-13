import pyaudio
import numpy as np
import speech_recognition as sr

from modules import color_print
class SpeechRecorder:
    def __init__(self):
        self.rate = 16000
        self.chunk = 1024
        self.silence_thresh = 300
        self.silence_sec = 2.5
        self.audio = pyaudio.PyAudio()
        self.recognizer = sr.Recognizer()
    
    def record_and_recognize(self):
        """Records voice and translates"""
        print("🎤 Записываю...")
        frames = []
        
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        silence_count = 0
        max_silence = int(self.silence_sec * self.rate / self.chunk)
        
        try:
            while silence_count < max_silence:
                data = stream.read(self.chunk, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                frames.append(data)
                
                if len(audio_data) > 0:
                    mean_squared = np.mean(audio_data**2)
                    rms = np.sqrt(mean_squared) if mean_squared > 0 else 0
                else:
                    rms = 0
                
                silence_count = 0 if rms > self.silence_thresh else silence_count + 1
                
        finally:
            stream.stop_stream()
            stream.close()
        
        if frames:
            return self._recognize(frames)
        return None
    
    def _recognize(self, frames):
        """Counting voice from frames"""
        try:
            audio_data = sr.AudioData(
                b''.join(frames), 
                self.rate, 
                self.audio.get_sample_size(pyaudio.paInt16)
            )
            return self.recognizer.recognize_google(audio_data, language="ru-RU")#return text
        except:
            color_print("No voice detected", 'yellow')
            return None


recorder = SpeechRecorder()