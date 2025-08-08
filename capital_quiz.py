# 나라 - 수도 퀴즈 (작성일: 2025.7.26 토)
# TODO: 결과 요약에 틀린 수도 목록 보여주기
# TODO: 틀린 문제에 가중치를 높이는 시스템

import re
import csv
import random
import os
from collections import defaultdict
from typing import List, Dict


QUIZ_COUNT = 10

# 입력값과 정답을 정규화하는 함수
def normalize(text: str):
    text = text.lower()
    text = text.replace(" ", "")
    text = re.sub(r'[^ㄱ-ㅎ가-힣a-z0-9]', '', text)
    return text


def is_correct(answer, user_input):
    return normalize(answer) == normalize(user_input)

def update_wrong_answers_csv(file_path: str, wrong_data: List[Dict[str, str]]):
    """
    file_path: 저장할 csv 파일 경로
    wrong_data: [{"country": "네팔", "capital": "카트만두"}, ...]
    """
    data_dict = defaultdict(lambda: {"count": 0})

    if os.path.exists(file_path):
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row["country"], row["capital"])
                data_dict[key]["count"] = int(row["count"])

    for item in wrong_data:
        key = (item["country"], item["capital"])
        data_dict[key]["count"] += 1

    with open(file_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["country", "capital", "count"])
        for (country, capital), info in data_dict.items():
            writer.writerow([country, capital, info["count"]])


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

    wrong_data = []  # 오답 저장 리스트

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

            # 오답 기록 추가
            wrong_data.append({"country": country, "capital": capital})
    
    # 오답 기록 업데이트
    wrong_file = './csv/wrong_answers.csv'
    update_wrong_answers_csv(wrong_file, wrong_data)
        
    percent = round((score / QUIZ_COUNT) * 100)

    print("\n📊 시험 결과 요약")
    print("────────────────────")
    print(f"✅ 맞힌 개수: {score} / {QUIZ_COUNT}")
    print(f"📈 점수 비율: {percent}%")

    # 피드백 메시지
    if percent == 100:
        print("🎉 만점입니다!")
