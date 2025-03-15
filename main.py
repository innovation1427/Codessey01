import tkinter as tk

def show_log():
    """로그 파일 내용을 GUI 창에 표시하는 함수"""
    try:
        with open('mission_computer_main.log', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = 'Error: 로그 파일을 찾을 수 없습니다.'
    except Exception as e:
        content = f'Error: {e}'

    # GUI 창 생성
    root = tk.Tk()
    root.title("Mission Computer Log")
    root.geometry("800x500")  # 창 크기 조절 (너비 800px, 높이 500px)

    # 텍스트 위젯
    text_widget = tk.Text(root, wrap="word", height=20, width=80)
    text_widget.insert("1.0", content)  # 파일 내용을 삽입
    text_widget.pack(expand=True, fill="both", side="left")

    # 스크롤바 추가
    scrollbar = tk.Scrollbar(root, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # 창 실행
    root.mainloop()

# 실행
show_log()
