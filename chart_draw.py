import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# 임의 데이터 생성 (여기서는 예시로 12개월의 매출 데이터 사용)
data = {
    "Month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "Sales": [200, 250, 300, 270, 320, 350, 400, 450, 380, 410, 450, 500]
}
df = pd.DataFrame(data)

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("Monthly Sales Chart")

# 월별 차트를 그리는 함수
def plot_chart(month):
    # 선택된 월에 해당하는 매출만 추출
    month_index = df[df["Month"] == month].index[0]
    
    # matplotlib 차트 생성
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df["Month"], df["Sales"])
    ax.set_title(f"Sales for {month}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    
    # 차트를 tkinter 윈도우에 넣기 위한 canvas 생성
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    
    # 기존 차트가 있으면 삭제
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# GUI 요소들
frame = ttk.Frame(root)
frame.pack(pady=10)

# 월을 선택하는 드롭다운 메뉴
month_label = ttk.Label(frame, text="Select Month:")
month_label.pack(side=tk.LEFT, padx=5)

month_combobox = ttk.Combobox(frame, values=df["Month"], state="readonly")
month_combobox.set("January")  # 기본값 설정
month_combobox.pack(side=tk.LEFT, padx=5)

# 차트 그리기 버튼
plot_button = ttk.Button(frame, text="Show Chart", command=lambda: plot_chart(month_combobox.get()))
plot_button.pack(side=tk.LEFT, padx=5)

# 차트를 보여줄 프레임
chart_frame = ttk.Frame(root)
chart_frame.pack(pady=20)

# 기본 차트 표시
plot_chart("January")

# Tkinter 메인 루프 시작
root.mainloop()
