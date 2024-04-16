# 열 순서를 바꾸는 코드 (24.4.15)
import csv

with open('filtered_result.csv', 'r') as f1, open('filtered_result_changed_header.csv', 'w') as f2:
    rdr = csv.reader(f1)
    wr = csv.writer(f2)
    old_header = next(rdr)
    new_header = ['제목', '작성일', '조회수', '추천수', '댓글수', '링크']
    col_length = len(new_header)
    wr.writerow(new_header)

    rows = list(rdr)
    for row in rows[:5]:
        new_row = [''] * col_length
        for idx in range(col_length):
            old_idx = old_header.index(new_header[idx])
            new_row[idx] = row[old_idx]
        wr.writerow(new_row)