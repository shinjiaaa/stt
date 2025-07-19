import pandas as pd

# 기존 메뉴 데이터 불러오기
df = pd.read_csv("./DATA/data.csv", encoding="cp949")

# 시니어 UI에서 사용할 메뉴만 필터링
senior_menu_names = [
    "카페모카", "카푸치노", "카라멜마끼아또", "할메가미숫커피",
    "자몽차", "유자차", "핫초코", "자몽주스",
    "허니브레드", "감자빵", "핫도그", "몽쉘케이크"
]

# 조건 필터링
senior_df = df[df["이름"].isin(senior_menu_names)].copy()

# 시니어 전용 번호 부여
senior_df.insert(0, "senior_no", range(1001, 1001 + len(senior_df)))

# CSV 파일로 저장
senior_df.to_csv("./DATA/senior_menu.csv", index=False, encoding="cp949")
print("senior_menu.csv 저장 완료")
