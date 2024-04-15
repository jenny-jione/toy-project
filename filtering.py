# csv 파일에서 특정 키워드가 들어간 행은 없애고 저장하는 코드 (24.4.15)

"""
csv 파일 형식
제목,댓글수,작성일,조회수,추천수,링크
"""
import csv

filtering_word = input()

with open('result.csv', 'r') as f, open(f'filtered_result_{filtering_word}.csv', 'w') as f2:
    rdr = csv.reader(f)
    wr = csv.writer(f2)
    header = next(rdr)
    wr.writerow(header)

    rows = list(rdr)
    before_len = len(rows)

    after_len = 0

    for row in rows:
        title = row[0]
        if filtering_word in title:
            continue
        after_len += 1
        wr.writerow(row)
    
    print(f'filtering completed: {before_len}->{after_len}')


