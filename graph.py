# 빈 날짜 채우기
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

with open('data.csv', 'r', encoding='utf-8-sig') as f:
    rdr = csv.reader(f)
    next(rdr)
    x = []
    y = []
    for rd in rdr:
        x.append(rd[0])
        y.append(rd[1])

print(x)

def plot_graph(x_values, y_values):
    # x 값 변환
    x_dates = [mdates.datestr2num(date) for date in x_values]
    
    # 그래프 그리기
    plt.plot(x_dates, y_values)
    
    # # x 축 포맷 설정
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # x 축 눈금을 일별로 설정
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d'))  # x 축 눈금 포맷 설정
    
    plt.xlabel('date')
    plt.ylabel('count')
    plt.title('graph')
    plt.show()

# 그래프 그리기
plot_graph(x, y)
