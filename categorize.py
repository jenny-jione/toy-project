# 크롤링한 글 CSV 파일의 카테고리 빈도 분석 및
# 텍스트 기반 차트 출력 (2025.6.19)

import csv
from collections import Counter

# CSV 파일에서 카테고리 카운트
def get_category_counts(filename):
    with open(filename, 'r') as f:
        rdr = csv.reader(f)
        header = next(rdr)
        category_index = header.index('category')
        
        data = list(rdr)
        category_counter = Counter()
        for row in data:
            category = row[category_index]
            category_counter[category] += 1
    return category_counter

# 비율 기반 블록 출력
def print_chart(counter):
    total = sum(counter.values())

    print("""
===== 결과 =====

⬜️ : 비율별 개수 (⬜️ 1개 = 1%)
예시) 27% → ⬜️ * 27개

-----------------
""".strip())

    for category, count in counter.most_common():
        percent = round((count / total) * 100)
        blocks = '⬜️' * percent
        print(f"{category}: \n{blocks} ({count}, {percent}%)\n")

# 실행
if __name__ == "__main__":
    counter = get_category_counts('./mypost.csv')
    print_chart(counter)