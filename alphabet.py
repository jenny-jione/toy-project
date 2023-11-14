# AA, AB, ..., Aa, ..., ZA, ... ZZ, ..., zz 까지 전부 출력하는 프로그램.
# 경우의 수: (26*2)*(26*2)
result = []

lower_a_code = ord('a')
lower_z_code = ord('z')
upper_a_code = ord('A')
upper_z_code = ord('Z')


for i in range(upper_a_code, upper_z_code+1):
    for j in range(upper_a_code, upper_z_code+1):
        char = chr(i) + chr(j)
        result.append(char)
    for k in range(lower_a_code, lower_z_code+1):
        char = chr(i) + chr(k)
        result.append(char)

for i in range(lower_a_code, lower_z_code+1):
    for j in range(upper_a_code, upper_z_code+1):
        char = chr(i) + chr(j)
        result.append(char)
    for k in range(lower_a_code, lower_z_code+1):
        char = chr(i) + chr(k)
        result.append(char)

# 한 줄에 n개씩 출력하는 함수.
def print_in_batches(data: list, n: int):
    for i in range(0, len(data), n):
        batch = data[i:i+n]
        print(batch)

ALPHABET_COUNT = 26

print_in_batches(result, ALPHABET_COUNT)

print(len(result))

print(result)