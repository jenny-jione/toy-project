# 특정 글에서 영어와 한글의 비율을 알려주는 프로그램 (2024.6.25)

import re
korean_regex = re.compile(r'[가-힣]')
english_regex = re.compile(r'[A-Za-z]')

def load_file():
    with open('./koreng_text.txt', 'r') as f:
        lines = f.readlines()
        data = [line.strip() for line in lines]
        return data

def count_characters(text: str):
    kor_cnt = len(korean_regex.findall(text))
    eng_cnt = len(english_regex.findall(text))
    return kor_cnt, eng_cnt

def calculate_proportions(total_kor, total_eng):
    if total_kor + total_eng == 0:
        print('[!] No characters found in the file.')
        return
    
    proportion_kor = round(total_kor / (total_kor + total_eng) * 100, 2)
    print(f'korean character count : {total_kor}')
    print(f'english character count: {total_eng}')
    print(f'proportion: {proportion_kor}%')

def main():
    data = load_file()
    if not data:
        print('[!] Text file is empty.')
        return

    total_kor, total_eng = 0, 0
    for text in data:
        kor_cnt, eng_cnt = count_characters(text)
        total_kor += kor_cnt
        total_eng += eng_cnt
    
    calculate_proportions(total_kor, total_eng)

if __name__ == "__main__":
    main()