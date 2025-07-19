from audio_helper import record_audio, save_wav, audio_to_text, detect_menu_items

duration = 5  # 예시 녹음 시간
menu_list = ["아이스 아메리카노", "핫 아메리카노", "연하게", "시럽"]

# 녹음
audio = record_audio(duration)

# 파일로 저장
wav_file = "recorded_audio.wav"
save_wav(wav_file, audio)

# 음성 -> 텍스트 변환
text_result = audio_to_text(wav_file)

print("인식 결과:", text_result)

# 메뉴 감지
cart = detect_menu_items(text_result, menu_list)
print("장바구니:", cart)
