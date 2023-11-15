# 시침, 분침, 초침 일치 시각 구하기

"""
분침이 1분동안 움직이는 단위를 1이라고 한다.
분침은 1시간에 한바퀴를 돈다. 
한바퀴는 60이다.
분침은 1시간(60분)동안 60을 움직인다.
시침은 12시간에 한바퀴를 돈다.
시침은 12시간(720분)동안 60을 움직인다.
시침은 24시간(1440분)동안 120을 움직인다.
시침은 1시간(60분)동안 5를 움직인다.
시침은 1분동안 5/60=1/12를 움직인다.
시침은 12분동안 1을 움직인다.
"""

for i in range(0, 720):
    hour = i // 60
    minute = i % 60
    hour_hand = i / 12
    minute_hand = i % 60
    # print(f'{hour}시 {minute}분 - 시침:{hour_hand}, 분침:{minute_hand}')
    if hour_hand == round(hour_hand, 0):
        print(f'{hour}시 {minute}분 - 시침:{hour_hand}, 분침:{minute_hand}')

# TODO: 초침도 추가하기. minute을 기준으로 하면 시침과 분침이 일치하는 시각이 0시 0분밖에 없음