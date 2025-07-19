import os
import time
import configparser

from pathlib import Path
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer
import streamlit as st
from model import RtzrAPI
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast


# config.ini에서 API 키 불러오기
def load_config(config_file="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config["RTZR"]["client_id"], config["RTZR"]["client_secret"]


@st.cache_resource()  # 모델 캐싱
def load_model():
    """허깅페이스 모델 불러오기"""
    model = BartForConditionalGeneration.from_pretrained("EbanLee/kobart-summary-v3")
    tokenizer = PreTrainedTokenizerFast.from_pretrained("EbanLee/kobart-summary-v3")
    return model, tokenizer


def stream_data(text: str) -> None:
    """텍스트를 한 단어씩 잘라서 Streamlit에 출력"""
    for word in text.split(" "):
        yield word + " "  # 단어 사이에 공백 추가 (단어 단위로 분리)


def file_upload_save(dir: str, upload_file) -> str:
    """녹음 파일을 로컬에 (임시) 저장"""
    os.makedirs(dir, exist_ok=True)
    path = Path(dir) / upload_file.name
    with open(path, "wb") as f:
        f.write(upload_file.read())
    return str(path)


def detect_menu_item(recognized_text: str, menu_list: list) -> list:
    """인식된 텍스트에서 메뉴 리스트에 있는 단어를 감지해 장바구니에 추가하는 함수"""
    cart = []
    for menu in menu_list:
        if menu in recognized_text:
            cart.append(menu)
    return cart


# 페이지 상단 UI & 오디오 녹음 컴포넌트
def page_setup(logo_url: str, homepage_url: str) -> bytes | None:
    st.markdown(
        f'[![Click me]({logo_url})]({homepage_url}) <span style="font-size:30px;">**Return Zero**</span>',
        unsafe_allow_html=True,
    )

    # 오디오 녹음 컴포넌트
    webrtc_ctx = webrtc_streamer(
        key="audio_recorder", media_stream_constraints={"audio": True, "video": False}
    )

    audio_bytes = None
    if webrtc_ctx.audio_receiver:
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        if audio_frames:
            audio_bytes = b"".join([frame.to_bytes() for frame in audio_frames])

    if audio_bytes:
        return audio_bytes
    else:
        return None


def process_audio_file(file_path):
    """WAV 파일을 받아서 텍스트로 변환"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(
                audio_data, language="ko-KR"
            )  # 한국어 인식
            return text
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"API 요청 오류: {e}"


def display_result(audio_file_path: str, audio_data) -> None:
    """결과 출력 페이지"""
    if audio_data is None:
        st.info("녹음을 시작해 주세요.")
        return

    try:
        client_id, client_secret = load_config()

        # 파일 저장
        file_path = file_upload_save(audio_file_path, audio_data)
        file_dict = {"file": (file_path, open(file_path, "rb"))}

        # API 호출
        api = RtzrAPI(
            client_id,
            client_secret,
            dev=False,
            file=file_dict,
            speaker_num=1,  # default
            domain="일반",
            profanity_filter=False,
            boost_keywords=[],
            model=st.session_state.model,
            tokenizer=st.session_state.tokenizer,
        )

        with st.spinner("음성을 처리 중입니다..."):
            while api.get_raw_data() is None:
                time.sleep(5)
                api.api_get()

            api.summary_inference()

            col1 = st.columns(1)[0]
            col1.markdown("## 변환된 텍스트")
            col1.container(border=True, height=400).write_stream(
                stream_data(api.get_text_data())
            )

            os.remove(file_path)  # 저장한 녹음 파일을 삭제 (임시 저장하는 거임)

    except Exception as e:
        st.error(f"error: {str(e)}")


# main
RTZR_LOGO_URL = "https://www.rtzr.ai/rtzr_logo.svg"
RTZR_HOMEPAGE_URL = "http://rtzr.ai"
AUDIO_FILE_PATH = "./resource"

st.set_page_config(layout="wide", page_title="STT", page_icon=RTZR_LOGO_URL)

if __name__ == "__main__":
    audio_data = page_setup(RTZR_LOGO_URL, RTZR_HOMEPAGE_URL)
    display_result(AUDIO_FILE_PATH, audio_data)
