# 나라와 수도 정보를 크롤링하여 저장하는 코드 (작성일: 2025.7.26 토)
# 결과는 ./csv/countries_and_capitals.csv 파일로 저장됩니다.

import csv
import os
import re
import requests
from bs4 import BeautifulSoup


URL = 'https://namu.wiki/w/%EC%88%98%EB%8F%84(%EB%8F%84%EC%8B%9C)/%EA%B5%AD%EA%B0%80%EB%B3%84'
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def clean_continent_title(raw_title: str):
    no_num = re.sub(r'^\d+\.\s*', '', raw_title)
    clean = re.sub(f'\[.*?\]', '', no_num).strip()
    return clean


def simple_parse_country_capital(div):
    a_tags = div.find_all('a')
    if len(a_tags) >= 2:
        country = a_tags[0].get_text(strip=True)
        capital = a_tags[1].get_text(strip=True)
        return country, capital
    return None, None


def get_info():
    response = requests.get(url=URL, headers=HEADERS)

    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    info_list = []
    
    # 모든 카테고리 div 찾기
    category_divs = soup.find_all('div', class_='UBV9xAVx ZxJhBjZZ')

    for category_div in category_divs:
        raw_title = category_div.get_text(strip=True)
        continent = clean_continent_title(raw_title)

        if '개요' in continent:
            continue

        if '사라진 나라의 수도' in continent:
            break

        # 다음 형제 요소 중 LX7a1vUt +C30O3Tm 찾기
        content_div = category_div.find_next_sibling('div', class_='LX7a1vUt +C30O3Tm')
        if content_div:
            for li in content_div.find_all('li'):
                info_div = li.find('div', class_='Ota8359y')
                if info_div:
                    country, capital = simple_parse_country_capital(info_div)
                    if country and capital:
                        info_list.append({
                            'continent': continent,
                            'country': country,
                            'capital': capital
                        })
                        print(info_list[-1])
    
    return info_list


def save_to_csv(data: list):
    with open('./csv/countries_and_capitals.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['continent', 'country', 'capital'])
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    try:
        data = get_info()
        os.makedirs('./csv', exist_ok=True)
        save_to_csv(data)

    except Exception as e:
        print(f"[ERROR] 데이터 수집 중 문제 발생: {e}")
