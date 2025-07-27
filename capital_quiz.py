# 나라 - 수도 퀴즈 (작성일: 2025.7.26 토)
# TODO: 사용자에게 대륙을 직접 선택하게 만드는 옵션
# TODO: 결과 요약에 틀린 수도 목록 보여주기
# TODO: 퀴즈 결과를 파일로 저장하기 (복습용)
# TODO: 틀린 문제에 가중치를 높이는 시스템

import csv
import random

QUIZ_COUNT = 10

with open('./csv/countries_and_capitals.csv', 'r', encoding='utf-8-sig') as f:
    rdr = csv.reader(f)
    next(rdr)

    target_continent = '유럽'
    data = [row for row in rdr if row[0] == target_continent]
    random.shuffle(data)

    score = 0

    for i in range(QUIZ_COUNT):
        continent, country, capital = data[i]
        answer = input(f"[{i+1}/{QUIZ_COUNT}] {country}의 수도는? ")

        if answer.strip() == capital:
            print(f"✅ 정답입니다! {country}의 수도는 {capital}입니다.\n")
            score += 1
        else:
            print(f"❌ 오답입니다! {country}의 수도는  {capital}입니다.")
            retry = input(f"다시 써보세요: {country}의 수도는? ")
            print()
        
    percent = round((score / QUIZ_COUNT) * 100)

    print("\n📊 시험 결과 요약")
    print("────────────────────")
    print(f"✅ 맞힌 개수: {score} / {QUIZ_COUNT}")
    print(f"📈 점수 비율: {percent}%")

    # 피드백 메시지
    if percent == 100:
        print("🎉 만점입니다!")
