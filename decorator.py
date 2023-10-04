# 함수의 실행시간을 측정하는 데코레이터
import time

def elapsed(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = f(*args, **kwargs)
        end = time.time()
        print("Elapsed time:", round(end-start, 4))
        return ret
    return wrapper

@elapsed
def add_numbers(num):
    result = 0
    for n in range(1, num+1):
        result += n
    return result

if __name__ == '__main__':
    add_numbers(100000000)