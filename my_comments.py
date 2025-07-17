# 댓글 크롤링 코드 (2025.7.16)
"""
크롤링할 정보
- 번호
- 글 제목
- 글 카테고리
- 댓글 내용
- 댓글 작성 날짜
- 링크
"""


import os
import time
from datetime import datetime
import csv

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv(verbose=True)

T_ID = os.getenv('T_ID')
T_PW = os.getenv('T_PW')
URL_LOGIN = os.getenv('URL_LOGIN')
URL_MY_COMMENT_PAGE = os.getenv('URL_MY_COMMENT_PAGE')
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
    한 페이지 내의 댓글 목록 크롤링하는 코드.

    리턴값
    [idx, category, title, comment, comment_date, post_link] 리스트 (한 페이지 분량씩 리턴)
    """

    table = driver.find_element(By.CLASS_NAME, 'table.table-striped.table-hover')
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    trs = tbody.find_elements(By.TAG_NAME, 'tr')

    result = []

    # 목록 순회
    for tr in trs:
        """
        전체 구조.
        <td>7730</td>
        <td>
				<p style="padding:0; margin:0; line-height: 20px;">
					게시글 :
                    <a href="/square" style="color:#999;">[스퀘어]</a> <a href="/url숫자" target="_blank">(글 제목)</a>
                </p>
				<p style="padding:0; margin:0; line-height: 20px;">
					내 댓글 : <a href="/url숫자#댓글위치" target="_blank">(댓글 내용)</a>
				</p>
			</td>
        <td>2025-07-16</td>
        <td> 체크박스 </td>
        """
        tds = tr.find_elements(By.TAG_NAME, 'td')[:-1]
        idx = tds[0].text

        p_tags = tds[1].find_elements(By.TAG_NAME, 'p')

        a_tags = p_tags[0].find_elements(By.TAG_NAME, 'a')
        if len(a_tags) < 2:
            category, title, post_link = '', '삭제된 글', ''
        else:
            a_cate, a_title = a_tags
            category = a_cate.text.strip('[]')
            title = a_title.text
            post_link = a_title.get_attribute('href')

        comment = p_tags[1].find_element(By.TAG_NAME, 'a').text

        comment_date = tds[2].text

        result.append([idx, category, title, comment, comment_date, post_link])

    return result


def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")
    log_file.write(f"[{now}] {msg}\n")


if __name__ == "__main__":
    
    options = webdriver.ChromeOptions()
    # headless 옵션을 추가하는 순간 계속 NoSuchElementException이 뜨는데 이 둘이 연관이 있나??? 그럴리가 없는데..
    options.add_argument('headless')
    
    options.add_argument("--window-position=1000,600")
    options.add_argument("--window-size=100,50")

    print("[INIT] ▶️ Chrome driver options:")
    print(f"        - headless: {'headless' in options.arguments}")
    print(f"        - window-position: 1000,600")
    print(f"        - window-size   : 100x50\n")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # # 쿠팡 크롤링 방지 설정을 undefined로 변경
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
    
    print("[INIT] 🚗 Launching browser and accessing login page...")
    driver.get(url=URL_LOGIN)

    print("[INIT] 🔍 Finding login elements...")
    driver.implicitly_wait(1)

    # 로그인
    driver.find_element(By.ID, "uid").send_keys(T_ID)
    driver.find_element(By.ID, "upw").send_keys(T_PW)
    driver.find_element(By.CLASS_NAME, "submit.btn.btn-inverse").click()
    time.sleep(0.3)

    # 비밀번호 변경 권장 페이지 닫기
    driver.find_element(By.ID, "hide-popup-checkbox").click()
    time.sleep(0.3)
    driver.find_element(By.ID, "close-popup-btn").click()
    time.sleep(0.5)

    # 작성글 보기 페이지
    driver.get(url=URL_MY_COMMENT_PAGE)
    time.sleep(0.3)
    last_page_num = get_last_page(driver)
    print(f"[INIT] 📄 Last page number: {last_page_num}")

    cnt = 0
    log_file = open(f'log_crawling_my_comments.txt', 'a')
    today_str = datetime.today().strftime('%Y-%m-%d')

    csv_path = f'result_comments_{T_ID}_test.csv'
    existing_rows = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            rdr = csv.reader(f)
            header = next(rdr)
            for row in rdr:
                existing_rows.append(row)
            latest_row = existing_rows[0]
            unique_key = '||'.join(latest_row[3:])
    else:
        header = ['idx', 'category', 'title', 'comment', 'comment_date', 'post_link']

    stop = False
    # 새로운 댓글
    new_rows = []
    for pagenum in range(1, last_page_num+1):
        log(f"▶️ Page {pagenum} crawling...")

        url = f'{URL_MY_COMMENT_PAGE}&page={pagenum}'
        driver.get(url)
        data = get_page_data(driver)

        for row in data:
            key = '||'.join(row[3:])
            if key == unique_key:
                stop = True
                log("⛔ Unique key found. Stopping crawl.")
                break
            new_rows.append(row)
        
        if stop:
            break

    # 데이터 저장
    all_rows = new_rows + existing_rows
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(all_rows)
    

    print('crawling finished.')
    print(f'saving {cnt} data finished.')
    print(f'result_{today_str}.csv')

    # 요약 출력
    print("\n📄 Crawling Summary")
    print("──────────────────────────────")
    print(f"🆕 New comments    : {len(new_rows)}")
    print(f"📦 Existing comments: {len(existing_rows)}")
    print(f"💾 Total saved      : {len(all_rows)}")
    log_file.write("\n📄 Crawling Summary\n")
    log_file.write("──────────────────────────────\n")
    log_file.write(f"🆕 New comments    : {len(new_rows)}\n")
    log_file.write(f"📦 Existing comments: {len(existing_rows)}\n")
    log_file.write(f"💾 Total saved      : {len(all_rows)}\n")


    driver.quit()