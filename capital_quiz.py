# 나라 - 수도 퀴즈 (작성일: 2025.7.26 토)
# TODO: 결과 요약에 틀린 수도 목록 보여주기
# TODO: 퀴즈 결과를 파일로 저장하기 (복습용)
# TODO: 틀린 문제에 가중치를 높이는 시스템

import re
import csv
import random

QUIZ_COUNT = 10

# 입력값과 정답을 정규화하는 함수
def normalize(text: str):
    text = text.lower()
    text = text.replace(" ", "")
    text = re.sub(r'[^ㄱ-ㅎ가-힣a-z0-9]', '', text)
    return text

def is_correct(answer, user_input):
    return normalize(answer) == normalize(user_input)

with open('./csv/countries_and_capitals.csv', 'r', encoding='utf-8-sig') as f:
    rdr = csv.reader(f)
    next(rdr)

    continents = ['아시아', '유럽', '아프리카', '북아메리카', '남아메리카', '오세아니아']
    while True:
        # 인풋을 숫자로 받아서 continents 리스트에서 인덱스로 선택하게 한다.
        print("🗺️  대륙 목록:")
        for i, continent in enumerate(continents, start=1):
            print(f"{i}. {continent}")
        print("0. ❌ 종료")
        choice = input("🔢 대륙을 선택하세요 (숫자 입력): ").strip()

        if choice == '0':
            print("프로그램을 종료합니다.")
            exit()
        if choice.isdigit() and 1 <= int(choice) <= len(continents):
            target_continent = continents[int(choice) - 1]
            break
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")

    data = [row for row in rdr if row[0] == target_continent]
    random.shuffle(data)

    score = 0

    print(f"\n🌍 {target_continent} 대륙의 수도 퀴즈를 시작합니다!")
    print(f"📋 총 {len(data)}개의 문제 중 {QUIZ_COUNT}개를 출제합니다.\n")
    print("✏️  문제에 대한 답을 입력해주세요.\n")

    for i in range(QUIZ_COUNT):
        continent, country, capital = data[i]
        answer = input(f"[{i+1}/{QUIZ_COUNT}] {country}의 수도는? ")

        if is_correct(capital, answer):
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
