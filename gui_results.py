from tkinter import *
from tkinter import ttk
import pandas as pd

def display_schedule_calendar(schedule_data):
    """ 달력 형식으로 근무 스케줄을 표시 """
    root = Tk()
    root.title("근무 스케줄")
    canvas = Canvas(root, width=700, height=500)
    canvas.pack()

    row_height = 50
    col_width = 100
    for i, date in enumerate(schedule_data.keys()):  
        x1, y1 = (i % 7) * col_width, (i // 7) * row_height
        x2, y2 = x1 + col_width, y1 + row_height
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        shifts = schedule_data[date]
        canvas.create_text(x1 + col_width/2, y1 + 10, text=date, font=("Arial", 10, "bold"))
        canvas.create_text(x1 + col_width/2, y1 + 25, text=f"D: {shifts.get('Day', '')}", font=("Arial", 8))
        canvas.create_text(x1 + col_width/2, y1 + 35, text=f"E: {shifts.get('Evening', '')}", font=("Arial", 8))
        canvas.create_text(x1 + col_width/2, y1 + 45, text=f"N: {shifts.get('Night', '')}", font=("Arial", 8))

    root.mainloop()

def save_schedule_to_excel(schedule_data, filename="schedule.xlsx"):
    """ 근무 스케줄 데이터를 엑셀 파일로 저장 """
    rows = []
    for date, shifts in schedule_data.items():
        for shift, nurse in shifts.items():
            rows.append({"Date": date, "Shift": shift, "Nurse": nurse})

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False, encoding="utf-8-sig")
    print(f"✅ 엑셀 파일이 저장되었습니다: {filename}")
