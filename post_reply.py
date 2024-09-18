# 특정 글의 댓글을 크롤링하는 코드 (2024.6.22)
"""
정보글의 경우 댓글도 유용한 경우가 많음.
크롤링할 정보
- 글 데이터
    - 정보글 제목
    - 작성 날짜
    - 링크
    - 조회수
    - 댓글수
- 댓글 데이터
    - 댓글 내용
    - 댓글 작성 날짜

TODO
1. 멘션의 경우 그 댓글 하위로 옮겨가게 하기 -> 2024.8.4 완료
    1
    2
    3
    21 @1

    1
        21
    2
    3
2. 본문 제목 정보도 넣기. -> 2024.8.5 완료
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
import re

load_dotenv(verbose=True)

T_ID = os.getenv('T_ID')
T_PW = os.getenv('T_PW')
URL_LOGIN = os.getenv('URL_LOGIN')
URL_MYPAGE = os.getenv('URL_MYPAGE')
URL = os.getenv('URL')
DOCUMENT_HEADER = os.getenv('DOCUMENT_HEADER')
SEP = os.getenv('SEP')


def get_page_data(driver: webdriver.Chrome):
    """
    해당 페이지 데이터 크롤링하는 코드.

    리턴값
    (title, post_date, link, views, reply_count)
    """

    # 제목
    div_header = driver.find_element(By.CLASS_NAME, DOCUMENT_HEADER)
    title = div_header.find_element(By.CLASS_NAME, 'title').text

    # 링크
    div_board = driver.find_element(By.CLASS_NAME, 'board.clear')
    div_side = div_board.find_element(By.CLASS_NAME, 'side')
    link = div_side.find_element(By.TAG_NAME, 'a').get_attribute('href')
    
    # 작성일
    div_sidefr = div_board.find_element(By.CLASS_NAME, 'side.fr')
    span = div_sidefr.find_element(By.TAG_NAME, 'span')
    print(span)
    # 날짜는 보류..안나옴-.-

    # 조회수, 댓글수
    div_count_container = div_board.find_element(By.CLASS_NAME, 'count_container')
    s = div_count_container.text
    view_count, reply_count = s.split()
    view_count = int(view_count.strip().replace(',', ''))
    reply_count = int(reply_count.strip())
    print('view_count:', view_count)
    print('reply_count:', reply_count)

    result = {
        'title': title,
        'link': link,
        'view_count': view_count,
        'reply_count': reply_count,
    }
    return result

def get_cur_reply_page(driver: webdriver.Chrome):
    ul_tag = driver.find_element(By.CLASS_NAME, 'fdb_lst_ul')
    cur_page = int(ul_tag.get_attribute('data-now-page'))
    print(f'crawling comments.. ({(cur_page-1)*100}-{cur_page*100})')
    li_comments = ul_tag.find_elements(By.TAG_NAME, 'li')
    result = []
    for li_comment in li_comments:
        # 댓글 번호
        div_meta = li_comment.find_element(By.CLASS_NAME, 'meta.virtual_comment')
        span_tag = div_meta.find_element(By.TAG_NAME, 'a').text
        reply_num = int(span_tag.split('. ')[0])

        # 댓글 작성 날짜
        span_date = div_meta.find_element(By.CLASS_NAME, 'date')
        reply_date = span_date.text

        # 댓글 내용
        div_comment = li_comment.find_elements(By.TAG_NAME, 'div')[1]
        reply_content = div_comment.text
        
        # div 태그의 모든 자식 태그 찾기
        child_tags = div_meta.find_elements(By.XPATH, './*')  
        reply_num_vice = ''
        if len(child_tags) == 3:
            strong_tag = div_meta.find_element(By.TAG_NAME, 'strong')
            reply_num_vice = strong_tag.text

        # reply_info = {
        #     'reply_num': reply_num,
        #     'reply_date': reply_date,
        #     'reply_content': reply_content,
        # }
        # result.append(reply_info)
        # keywords = ['ㅅ', '삭제된 댓글입니다', '스크랩']
        # if any(keyword in reply_content for keyword in keywords):# or len(reply_content)<10:
        #     continue
        result.append([reply_num, reply_num_vice, reply_date, reply_content])
    print('len:', len(result))
    return result

# 대댓글 찾는 함수 (더이상 대댓글이 없을 때까지 재귀호출됨)
# TODO: wr변수가 csv.writer(f)인데 파라미터로 보낼 때 타입 힌팅 하는 법
def search_child(cur: int, rereply_info: dict, depth: int, reply_data: list, wr):
    rn, rv, rd, rt = reply_data[cur]
    child_cnt = len(rereply_info[cur]['child'])
    row = [rn, rv, rd, 'ㄴ'*depth + rt, child_cnt]
    wr.writerow(row)
    if not rereply_info[cur]['child']:
        return
    for my_child in rereply_info[cur]['child']:
        search_child(my_child, rereply_info, depth+1, reply_data, wr)
    return

# 
def process_rereply(filename):
    rereply_info = {}
    with open(f'{filename}.csv', 'r') as f:
        rdr = csv.reader(f)
        reply_data = [row for row in rdr]
    cnt = len(reply_data)
    rereply_info = {i:{'parent': [], 'child': []} for i in range(1, cnt)}
    for row in reply_data[1:]:
        rnum, rvice, rdate, rtxt = row
        rnum = int(rnum)
        # 글자 없이 이미지만 올릴 경우 rtxt가 빈 문자열임.
        if not rtxt:
            continue
        if rtxt[0] == '☞':
            parent_num = int(rtxt.split(SEP)[0].strip('☞'))
            child_num = rnum
            rereply_info[parent_num]['child'].append(child_num)
            rereply_info[child_num]['parent'].append(parent_num)
    
    with open(f'{filename}__rereply.csv', 'w') as f2:
        wr = csv.writer(f2)
        # 헤더: 댓글 번호, 댓글 작성자 식별, 댓글 작성시각, 댓글 내용, 대댓글 개수
        header = ['no', 'vice', 'date', 'comment', 'rereply_count']
        wr.writerow(header)
        for rnum, value in rereply_info.items():
            if not value['parent']:
                # child(대댓글)가 존재할 경우 대댓글 찾기 함수 호출 (재귀호출됨)
                if value['child']:
                    search_child(rnum, rereply_info, 0, reply_data, wr)
                else:
                    wr.writerow([*reply_data[rnum], 0])

if __name__ == "__main__":

    url = input('Please enter the url:')
    
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    # 창의 위치
    options.add_argument("--window-position=1000,600")
    # 창의 크기
    options.add_argument("--window-size=100,50")

    # 
    print('option ::')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # # 크롤링 방지 설정을 undefined로 변경
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

    # 사용자가 입력한 url 페이지
    driver.get(url=url)
    time.sleep(0.3)

    # 해당 글 정보
    page_info = get_page_data(driver)
    title = page_info.get('title')

    # 댓글
    # (댓글 수를 100으로 나눈 몫) 만큼 '댓글 더 보기' 눌러야 함
    click_num = (page_info.get('reply_count')//100)
    
    reply_data = []
    data = get_cur_reply_page(driver)
    reply_data.extend(data)
    for i in range(click_num):
        driver.find_element(By.CLASS_NAME, 'show_more.comment_header').click()
        time.sleep(0.3)
        reply_data.extend(get_cur_reply_page(driver))
    
    # 댓글 번호 오름차순으로 정렬
    reply_data.sort(key=lambda x:x[0])

    today_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    uid = url.split('/')[-1]
    filename = f'result_{today_str}_{uid}_{title}'
    with open(f'{filename}.csv', 'w') as f:
        wr = csv.writer(f)
        header = ['no', 'vice' 'date', 'comment']
        wr.writerow(header)

        for rd in reply_data:
            wr.writerow(rd)
    
    print('crawling finished.')
    print(f'saving {len(reply_data)} data finished.')

    driver.quit()

    process_rereply(filename)
    print('processing rereply successfully finished.')