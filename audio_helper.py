import sounddevice as sd
import wave
import speech_recognition as sr


# WAV 저장 함수
def save_wav(filename, data, samplerate=44100):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16bit
        wf.setframerate(samplerate)
        wf.writeframes(data.tobytes())


# 녹음 함수 (duration 초 동안 녹음)
def record_audio(duration, samplerate=44100):
    audio = sd.rec(
        int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16"
    )
    sd.wait()
    return audio


# 음성 파일을 텍스트로 변환하는 함수
def audio_to_text(wav_filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ko-KR")
            return text
        except sr.UnknownValueError:
            return "❌ 음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"❌ API 요청 오류: {e}"


# 메뉴 리스트에서 인식된 메뉴 감지 함수
def detect_menu_items(recognized_text, menu_list):
    cart = []
    for menu in menu_list:
        if menu in recognized_text:
            cart.append(menu)
    return cart
