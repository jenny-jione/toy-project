# 내가 쓴 글을 크롤링하는 코드 (2024.5.14)
"""
크롤링할 정보
- 글 제목
- 카테고리
- 작성 날짜
- 링크
- 번호
- 조회수
- 댓글수
"""

import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import datetime
import csv

load_dotenv(verbose=True)

T_ID = os.getenv('T_ID')
T_PW = os.getenv('T_PW')
URL_LOGIN = os.getenv('URL_LOGIN')
URL_MYPAGE = os.getenv('URL_MYPAGE')
URL = os.getenv('URL')


def get_last_page(driver: webdriver.Chrome):
    pagination = driver.find_element(By.CLASS_NAME, 'pagination')
    li_tag = pagination.find_elements(By.TAG_NAME, 'li')[-1]
    a_tag = li_tag.find_element(By.TAG_NAME, 'a')
    url = a_tag.get_attribute('href')
    lastpage = int(url.split('=')[-1])
    return lastpage


def get_page_data(driver: webdriver.Chrome):
    """
    크롤링 코드.

    리턴값
    """

    table = driver.find_element(By.CLASS_NAME, 'table.table-striped.table-hover')
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    trs = tbody.find_elements(By.TAG_NAME, 'tr')
    print(type(trs))
    print(len(trs))

    # 목록 순회
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')[:-1]
        idx = tds[0].text
        td_title = tds[1]
        title_raw = td_title.text
        category = title_raw.split(']')[0].strip('[')
        splited = title_raw.split('[')
        if len(splited) == 2:
            reply_num = 0
        else:
            reply_num = splited[-1].strip(']')
        title = splited[1].split(']')[1].strip()
        a_tag = td_title.find_elements(By.TAG_NAME, 'a')[1]
        link = a_tag.get_attribute('href')
        post_date = tds[2].text
        result.append([idx, category, title, post_date, reply_num, link])
    return result


def save_file(data: list):
    today_str = datetime.today().strftime('%Y-%m-%d')
    with open(f'result_{today_str}.csv', 'w') as f:
        wr = csv.writer(f)
        header = ['product_name', 'product_price', 'order_date', 'status']
        wr.writerow(header)
        for row in data:
            wr.writerow(row)


if __name__ == "__main__":
    
    options = webdriver.ChromeOptions()
    # headless 옵션을 추가하는 순간 계속 NoSuchElementException이 뜨는데 이 둘이 연관이 있나??? 그럴리가 없는데..
    # options.add_argument('headless')
    # 창의 위치
    options.add_argument("--window-position=1000,600")
    # 창의 크기
    options.add_argument("--window-size=100,50")

    # 
    print('option ::')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # # 쿠팡 크롤링 방지 설정을 undefined로 변경
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
    
    driver.get(url=URL_LOGIN)
    print('driver get url')
    print('finding login element ... ')
    driver.implicitly_wait(1)

    # 로그인
    driver.find_element(By.ID, "uid").send_keys(T_ID)
    driver.find_element(By.ID, "upw").send_keys(T_PW)
    driver.find_element(By.CLASS_NAME, "submit.btn.btn-inverse").click()
    time.sleep(0.3)

    # 작성글 보기 페이지
    driver.get(url=URL_MYPAGE)
    time.sleep(0.3)
    last_page_num = get_last_page(driver)

    result = []

    # for pagenum in range(1, last_page_num+1):
    for pagenum in range(62, 63):
        url = f'{URL}&page={pagenum}'
        driver.get(url)
        get_page_data(driver)
    
    print('crawling finished.')

    save_file(result)
    print(f'saving {len(result)} data finished.')

    driver.quit()

"""
TODO
1. 대괄호 기준으로 split하기
    [카테고리이름] 제목 [댓글수] 일 때
    카테고리이름/제목/댓글수 로 나뉘어야 함
    근데 댓글이 없는 경우에는
    [카테고리이름] 제목 
    으로만 되어 있음
"""