# 1의 자리만 표시된 리스트가 주어질 경우, 조건을 만족하는 모든 숫자 조합을 찾는다.
# ex) num = [6, 5, 7, 5, 6]이 주어질 경우 만족하는 숫자 조합은 아래와 같다.
# [6, 15, 17, 25, 26]
# [6, 15, 17, 25, 36]
# [6, 15, 17, 35, 36]
# [6, 15, 27, 35, 36]
# [6, 25, 27, 35, 36]
# [16, 25, 27, 35, 36]


num = [6, 5, 7, 5, 6]
leng = len(num)
MAX_NUM = 45

result = []

# 재귀함수 이용
def ltry_recur(start_num: int, cur_idx: int, nli: list):
    if (cur_idx >= leng) or (start_num > MAX_NUM):
        if len(nli) >= leng:
            result.append(nli)
        return nli
    for n in range(start_num, MAX_NUM+1):
        n_1 = n % 10
        if num[cur_idx] == n_1:
            ltry_recur(n+1, cur_idx+1, nli+[n])
    return nli


# stack 이용
def ltry_stack(start_num: int, cur_idx: int, nli: list):
    stack = [(start_num, cur_idx, nli)]

    while stack:
        start_num, cur_idx, nli = stack.pop()

        if cur_idx >= leng or start_num > MAX_NUM:
            if len(nli) >= leng:
                result.append(nli)
        else:
            for n in range(start_num, MAX_NUM + 1):
                n_1 = n % 10
                if num[cur_idx] == n_1:
                    stack.append((n + 1, cur_idx + 1, nli + [n]))


import time

t1 = time.time()
ltry_stack(start_num=1, cur_idx=0, nli=[])
t2 = time.time()
print("Elapsed time(stack):", round(t2-t1))

t1 = time.time()
ltry_recur(start_num=1, cur_idx=0, nli=[])
t2 = time.time()
print("Elapsed time(recur):", round(t2-t1, 4))

all_cases = len(result)
if all_cases < 100:
    for res in result:
        print(res)
print(all_cases)

# cases = []
# for res in result:
#     for lastnum in range(1, 46):
#         if lastnum not in res:
#             casee = res[:] + [lastnum]
#             cases.append(sorted(casee))

# for c in cases:
#     print(c)
# print(len(cases))  

# # -- 출력을 위한 정렬. 구현 알고리즘과는 관련 없음. --
# cases_sorted = sorted(cases, key=lambda x: x[0])

# for c in cases_sorted:
#     print(c)

# print(len(cases_sorted))