# 2025-06-11 20:09:42 형식으로 랜덤 시각을 생성해주는 코드

import random
from datetime import datetime

# 기본 날짜 설정 (예: 2025년 1월 1일)
default_dt = "250101"

# 사용자 입력
dt = input("yymmdd:")

# 입력 유효성 확인 없이 시도 -> 실패하면 기본값 사용
try:
    date_obj = datetime.strptime(dt, "%y%m%d")
except Exception:
    print("잘못된 형식이므로 기본 날짜(250101)로 처리합니다.")
    date_obj = datetime.strptime(default_dt, "%y%m%d")

# 시간대 입력
try:
    start_hour = int(input("시작 시(hour, 0~23): "))
    end_hour = int(input("종료 시(hour, 0~23): "))

    if not (0 <= start_hour <= 23 and 0 <= end_hour <= 23) or start_hour > end_hour:
        raise ValueError
except Exception:
    print("잘못된 시각 범위이므로 기본 범위(17~23시)로 설정합니다.")
    start_hour = 17
    end_hour = 23

# 랜덤 시각 생성
for _ in range(10):
    hour = random.randint(17, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    time_str = f"{hour:02}:{minute:02}:{second:02}"
    print(f"{date_obj.strftime('%Y-%m-%d')} {time_str}")