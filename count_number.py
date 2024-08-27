# 숫자를 한국어로 세는 프로그램 (24.8.27)
"""
input : 12315678109071
output: 십이조 삼천백오십육억 칠천팔백십만 구천칠십일
"""
num = input()
print(num)
rev_num = num[::-1]

post = ['', '십', '백', '천']

unit = ['', '만', '억', '조', '경', '해', 
        '자', '양', '구', '간', '정', '재', '극',
        '항하사', '아승기', '나유타', '불가사의', '무량대수']

number = {
    '1': '일',
    '2': '이',
    '3': '삼',
    '4': '사',
    '5': '오',
    '6': '육',
    '7': '칠',
    '8': '팔',
    '9': '구',
    '0': ''
}

N = 4

r = len(num) % N
rev_num_chunk = [rev_num[i*N:(i+1)*N] for i in range((len(num)-1)//N+1)]

num_chunk = [i[::-1] for i in rev_num_chunk][::-1]
print(*num_chunk)
print(*num_chunk, sep=',')

stack = []
for u, chunk in enumerate(rev_num_chunk):
    if u > 0:
        stack.append(f'({unit[u]}) ')
    for i, n in enumerate(chunk):
        if n == '0':
            continue
        if n == '1' and i > 0:
            res = ''
        else:
            res = number[n]
        res += post[i]
        stack.append(res)

print(''.join(stack[::-1]))