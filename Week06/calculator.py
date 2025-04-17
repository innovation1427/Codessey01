# calculator.py
import sys  # 시스템 관련 함수와 인수 처리용
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit  # PyQt5에서 필요한 위젯들을 임포트
from PyQt5.QtCore import Qt  # Qt 모듈에서 유용한 정렬 속성을 임포트

class Calculator(QWidget):
    def __init__(self):
        super().__init__()  # QWidget의 생성자 호출
        self.setWindowTitle("계산기")  # 윈도우의 제목을 "계산기"로 설정
        self.setFixedSize(300, 400)  # 계산기 창의 고정 크기를 300x400으로 설정
        self.init_ui()  # UI 초기화 함수 호출

    def init_ui(self):
        # 입력창 설정
        self.display = QLineEdit()  # QLineEdit 위젯을 사용해 계산 결과를 표시할 입력창 생성
        self.display.setAlignment(Qt.AlignRight)  # 입력창의 텍스트를 오른쪽 정렬
        self.display.setReadOnly(True)  # 입력창을 읽기 전용으로 설정, 사용자가 직접 입력하지 못하게 함
        self.display.setFixedHeight(50)  # 입력창의 높이를 고정
        self.display.setStyleSheet("font-size: 24px;")  # 폰트 크기를 24px로 설정

        # 버튼 배열 설정 (버튼의 텍스트 배열)
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 레이아웃 설정
        main_layout = QVBoxLayout()  # 수직 레이아웃을 생성
        grid_layout = QGridLayout()  # 그리드 레이아웃을 생성
        main_layout.addWidget(self.display)  # 수직 레이아웃에 입력창을 추가
        main_layout.addLayout(grid_layout)  # 그리드 레이아웃을 수직 레이아웃에 추가
        self.setLayout(main_layout)  # 계산기의 전체 레이아웃 설정

        # 버튼 생성 및 배치
        for row, row_values in enumerate(buttons):  # buttons 리스트의 각 행을 반복
            for col, val in enumerate(row_values):  # 각 버튼 값을 반복
                if val == '0':  # 0 버튼은 두 칸 차지하도록 배치
                    btn = QPushButton(val)  # 버튼 생성
                    btn.setFixedHeight(50)  # 버튼의 높이 고정
                    btn.setStyleSheet("font-size: 18px;")  # 버튼의 글자 크기 설정
                    grid_layout.addWidget(btn, row + 1, col, 1, 2)  # 두 칸을 차지하는 0 버튼
                    btn.clicked.connect(self.button_clicked)  # 버튼 클릭 시 button_clicked 함수 연결
                elif val == '.':  # . 버튼은 3번째 칸에 배치
                    btn = QPushButton(val)
                    btn.setFixedHeight(50)
                    btn.setStyleSheet("font-size: 18px;")
                    grid_layout.addWidget(btn, row + 1, col + 1)  # 3번째 칸에 배치
                    btn.clicked.connect(self.button_clicked)
                elif val == '=':  # = 버튼은 결과를 계산하는 버튼
                    btn = QPushButton(val)
                    btn.setFixedHeight(50)
                    btn.setStyleSheet("font-size: 18px;")
                    grid_layout.addWidget(btn, row + 1, col + 1)  # = 버튼 배치
                    btn.clicked.connect(self.calculate)  # 계산 함수 연결
                else:  # 나머지 숫자 및 연산자 버튼들
                    btn = QPushButton(val)
                    btn.setFixedHeight(50)
                    btn.setStyleSheet("font-size: 18px;")
                    grid_layout.addWidget(btn, row + 1, col)  # 기본 버튼 배치
                    btn.clicked.connect(self.button_clicked)  # 버튼 클릭 시 button_clicked 함수 연결

    def button_clicked(self):
        sender = self.sender()  # 클릭된 버튼을 가져옴
        current = self.display.text()  # 현재 입력창의 텍스트를 가져옴
        text = sender.text()  # 클릭된 버튼의 텍스트를 가져옴

        # 버튼이 숫자나 연산자일 경우 입력창에 추가
        if text == 'AC':  # AC 버튼 클릭 시 입력창 초기화
            self.display.clear()
        elif text == '+/-':  # 부호 변경 버튼 클릭 시
            if current and current[0] == '-':  # 현재 값이 음수라면 부호 제거
                self.display.setText(current[1:])
            else:  # 현재 값이 양수라면 부호 추가
                self.display.setText('-' + current)
        else:  # 그 외 숫자나 연산자는 입력창에 추가
            self.display.setText(current + text)

    def calculate(self):
        # 입력된 수식 계산하기
        try:
            current_text = self.display.text()  # 입력된 텍스트 가져오기
            if current_text:  # 수식이 비어있지 않다면
                # eval()로 수식을 계산하고 결과를 출력
                result = eval(current_text.replace('÷', '/').replace('×', '*'))  # ÷는 /로, ×는 *로 변환
                self.display.setText(str(result))  # 결과를 입력창에 출력
        except Exception as e:
            self.display.setText('Error')  # 오류 발생 시 "Error" 출력

# 애플리케이션 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    calc = Calculator()  # 계산기 객체 생성
    calc.show()  # 계산기 화면 표시
    sys.exit(app.exec_())  # 애플리케이션 실행
