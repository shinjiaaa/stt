import streamlit as st
import sounddevice as sd
import numpy as np
import wave
from utils import process_audio_file


# 장바구니에 메뉴 감지하는 함수
def detect_menu_item(recognized_text: str, menu_list: list) -> list:
    cart = []
    for menu in menu_list:
        if menu in recognized_text:
            cart.append(menu)
    return cart


# WAV 저장 함수
def save_wav(filename, data, samplerate=44100):
    """녹음 데이터를 WAV로 저장"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16bit
        wf.setframerate(samplerate)
        wf.writeframes(data.tobytes())


# Streamlit UI
st.title("STT")
st.write("**[Start Recording]** 버튼을 누르면 녹음이 시작됩니다.")

duration = st.number_input("녹음 시간 (초)", min_value=1, max_value=60, value=5, step=1)

# 예시 메뉴 리스트 (추후 GUI랑 연동하여 GUI 내에 있는 단어로 리스트 채워야 함)
menu_list = ["아이스 아메리카노", "핫 아메리카노", "연하게", "시럽"]

if st.button("🎤 Start Recording"):
    st.info("녹음 중입니다...")
    samplerate = 44100
    audio = sd.rec(
        int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16"
    )
    sd.wait()

    output_file = "recorded_audio.wav"
    save_wav(output_file, audio, samplerate)

    st.success("녹음 완료! 음성을 처리 중입니다...")

    text_result = process_audio_file(output_file)
    st.subheader("변환 결과")
    st.write(text_result)

    # 장바구니 감지
    cart_items = detect_menu_item(text_result, menu_list)
    st.subheader("장바구니에 담긴 메뉴")
    if cart_items:
        st.write(cart_items)
    else:
        st.write("인식된 메뉴가 없습니다.")
