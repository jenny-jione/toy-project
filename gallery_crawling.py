# 갤러리 크롤링 (2024.4.14)
"""
TODO
1. 관심없는 키워드가 들어간 글은 아예 건너뛰거나 따로 표시하기 ==> filtering.py로 구현함
2. 반대수는 각각의 글을 직접 들어가야 알 수 있는 거라서.. 이건 생각해보기
3. save_file 안에 매번 with open 하지 말고 밖에서 exist 확인해서 save_file의 파라미터로 wr 가져가기
4. 크롤링 중에 종료되는 경우가 있는데 자동으로 재시작할 수 있는 방법 없나??
5. 크롤링 시작 전에 전체 페이지 수 구하는 부분 추가하기 ==> 완료
6. 이미 있는 csv 파일의 경우 헤더 추가 코드 없음. 새로 csv 파일을 생성하는 경우에만 header 넣기 ==> 완료
7. 작성자 ip도 크롤링할지??
8. 클래스화 ??
9. 이미 수집한 csv 파일 특정 열 기준으로 정렬하는 함수 작성하기 result_{gallery_name}_sorted_by_{정렬기준}.csv
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
from datetime import datetime
import re
import os

TIME_SLEEP = 0.3


def get_total_page(driver: webdriver.Chrome, gallery_name: str):
    print(f'get total page .. gallery name: {gallery_name}')
    url = f'https://gall.dcinside.com/mgallery/board/lists/?id={gallery_name}&exception_mode=recommend'
    driver.get(url)
    print('find element .. ')
    page_end_tag = driver.find_element(By.CLASS_NAME, "sp_pagingicon.page_end")
    href = page_end_tag.get_attribute('href')
    pattern = r'\d+'
    regex_result = re.findall(pattern, href)
    total_page = int(regex_result[0])
    return total_page


def get_data(driver: webdriver.Chrome, gallery_name: str, page: int):
    print(f'page={page} crawling ...')
    url=f'https://gall.dcinside.com/mgallery/board/lists/?id={gallery_name}&page={page}&exception_mode=recommend'
    driver.get(url)
    time.sleep(TIME_SLEEP)

    # table 찾기
    table_tag = driver.find_element(By.CLASS_NAME, "gall_list")

    # 글 목록 (trs: 한 페이지 안에 있는 모든 글의 리스트)
    trs = table_tag.find_elements(By.CLASS_NAME, "ub-content.us-post")
    print(f'{len(trs)} data were successfully crawled.')

    result = []
    # 목록 순회. tr은 한 행(개념글 하나)
    for tr in trs:
        # tr은 여러개의 td로 이루어짐 - (번호|말머리|제목|글쓴이|작성일|조회|추천)
        # 크롤링할 데이터: 제목, 댓글수, 작성일, 조회수, 추천수, 게시물 링크
        
        # gall_tit.ub-word는 제목 td이고 2개의 <a>로 이루어져 있음 (제목+댓글수)
        td_title = tr.find_element(By.CLASS_NAME, "gall_tit.ub-word")
        a_tags = td_title.find_elements(By.TAG_NAME, "a")

        # 게시물 링크
        href = a_tags[0].get_attribute('href')

        title = a_tags[0].text
        # 댓글이 없는 경우 a_tags의 길이는 1이므로 따로 처리해주어야 함.
        if len(a_tags) == 1:
            reply_count = 0
        else:
            # 보이스리플이 있는 경우 [14/1] 이런 형식으로 나타난다.. 그래서 이 경우도 따로 분류해주어야 함.
            repl_raw = a_tags[1].text
            if '/' in repl_raw:
                reply_count = int(repl_raw[1:].split('/')[0])
            else:
                reply_count = int(a_tags[1].text[1:-1])

        # 작성일
        td_date = tr.find_element(By.CLASS_NAME, "gall_date")
        post_date = td_date.text

        # 조회수
        td_view = tr.find_element(By.CLASS_NAME, "gall_count")
        view_count = int(td_view.text)

        # 추천수
        td_recommand = tr.find_element(By.CLASS_NAME, "gall_recommend")
        recommand_count = int(td_recommand.text)

        result.append([title, post_date, view_count, recommand_count, reply_count, href])
        # 확인용 print문. 생략 가능
        # print(result[-1][:-1])
    return result
        

def save_file(data: list, gallery_name: str, mode: str):
    filename = f'result_{gallery_name}'
    HEADER = ['제목', '작성일', '조회수', '추천수', '댓글수', '링크']
    if mode == 'test':
        with open(f'{filename}_test.csv', 'w') as f:
            wr = csv.writer(f)
            wr.writerow(HEADER)
            for row in data:
                wr.writerow(row)

    elif mode == 'all':
        fn = f'{filename}_all.csv'
        # 이전에 크롤링한 적 있는지 확인 (header writerow 여부)
        newly = False
        if not os.path.exists(fn):
            newly = True
        with open(fn, 'a') as f:
            wr = csv.writer(f)
            if newly:
                wr.writerow(HEADER)
            for row in data:
                wr.writerow(row)
    else:
        print(' *** wrong mode :: please check mode again. ***')


if __name__ == "__main__":

    test_mode = False
    print(f'test_mode?', test_mode)
    gallery_name = input()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    print('driver ...')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    total_page = get_total_page(driver, gallery_name)
    print(f'total {total_page} page')

    # 특정 페이지 크롤링 (테스트용)
    if test_mode:
        data = get_data(driver, gallery_name, total_page)
        save_file(data, gallery_name, mode='test')
        print('crawling successfully finished.')
        driver.quit()
    
    # 1~total_page 전체 페이지 크롤링
    else:
        log_file = open(f'log_crawling_{gallery_name}.txt', 'a')

        print('[ crawling start ]')

        # for page in range(total_page, 0, -1):
        for page in range(total_page, total_page-2, -1):
            data = get_data(driver, gallery_name, page)
            save_file(data, gallery_name, mode='all')
            current_time: datetime = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(formatted_time + '\t' + str(page) + ' page\n')
        
        driver.quit()


