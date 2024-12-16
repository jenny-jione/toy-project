# 2024.12.16
# safari에 저장된 북마크 중 삭제된 링크는 없애고 유효한 링크만 남기는 코드.
import requests
import re

def code302(url: str, title: str):
    try:
        response = requests.get(url, allow_redirects=False)  # 리다이렉션 금지
        if response.status_code == 302:
            # print(f"링크가 302 Found 상태를 반환했습니다: {url}")
            print(f'deleted :: {title[:10]}.. {url}')
            return True
        else:
            # print(f"링크 상태 코드: {response.status_code}")
            print(f'alive   :: {title[:10]}.. {url}')
            return False
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
        return False


cnt = 0
website = ['heqoo', 'pann', 'inside']

p_all = 0
p_deleted = 0
p_alive = 0

alive = []
deleted = []

with open('./bookmark.txt', 'r') as f1, open('./bookmark_cleaned.txt', 'w') as f2:
    for i, line in enumerate(f1):
        print(f'{i}\t{p_all}({p_alive}+{p_deleted})')
        match = re.search(r'<A HREF="([^"]+)">(.*?)</A>', line)
        if match:
            url = match.group(1)
            title = match.group(2)
            if 'pann' in url:
                p_all += 1
                if code302(url, title):
                    p_deleted += 1
                    deleted.append(url)
                    continue
                p_alive += 1
                alive.append(url)
                f2.write(line)
            cnt += 1
        else:
            f2.write(line)

print(p_all)
print(p_alive)
print(p_deleted)


print()
print('--alive--')
for u in alive:
    print(u)
print()


print('--deleted--')
for u in deleted:
    print(u)