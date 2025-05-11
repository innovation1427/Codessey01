import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout
from PySide6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("계산기")
        self.setFixedSize(390, 650)
        self.setStyleSheet("background-color: black;") # 배경

        self.first_number = ''
        self.second_number = ''
        self.operator = ''
        self.result = ''

        self.init_ui()

    def init_ui(self):
        self.display = QLabel('0') # 기본 값 0
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter) # 텍스트가 오른쪽, 수직 중앙 정렬
        self.display.setStyleSheet("color: white; font-size: 64px; padding: 30px 10px 10px 10px;") # 텍스트

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout() # 그리드 형식 배치
        grid.setSpacing(10) # 버튼 간격 10px로 설정

        # 배열을 행 기준으로 순차적으로 반복하며 버튼을 QPushButton 객체로 생성
        for row, line in enumerate(buttons):
            col = 0
            for text in line:
                btn = QPushButton(text)
                if text == '0':     # 0 버튼은 두 칸을 차지하도록 설정
                    btn.setFixedSize(170, 80)
                    grid.addWidget(btn, row + 1, col, 1, 2)
                    col += 1
                else:
                    btn.setFixedSize(80, 80)
                    grid.addWidget(btn, row + 1, col, 1, 1)

                btn.setStyleSheet(self.get_style(text))  # 버튼에 스타일 적용
                btn.clicked.connect(lambda _, t=text: self.button_clicked(t)) # lambda**를 사용하여 버튼 텍스트(t)를 인자로 넘김
                col += 1

        layout = QVBoxLayout() # 수직 레이아웃 생성
        layout.addWidget(self.display) # 입력창 상단에 추가
        layout.addLayout(grid) # 그리드 레이아웃을 입력창 아래에 추가
        self.setLayout(layout)

    # 버튼의 텍스트에 따라 버튼 스타일 정의
    def get_style(self, text):
        if text in ['AC', '+/-', '%']:
            return self.style_function_btn()
        elif text in ['+', '-', '×', '÷', '=']:
            return self.style_operator_btn()
        else:
            return self.style_number_btn()

    def style_function_btn(self):
        return """
        QPushButton {
            background-color: #D4D4D2;
            color: black;
            border: none;
            border-radius: 40px;
            font-size: 28px;
        }
        QPushButton:pressed {
            background-color: #BFBFBD;
        }"""
    
    def style_operator_btn(self):
        return """
        QPushButton {
            background-color: #FF9500;
            color: white;
            border: none;
            border-radius: 40px;
            font-size: 28px;
        }
        QPushButton:pressed {
            background-color: #CC7A00;
        }"""
    
    def style_number_btn(self):
        return """
        QPushButton {
            background-color: #505050;
            color: white;
            border: none;
            border-radius: 40px;
            font-size: 28px;
        }
        QPushButton:pressed {
            background-color: #707070;
        }"""

    # 버튼 클릭시 이벤트 추가
    def button_clicked(self, key):
        actions = {
            'AC': self.reset,
            '+/-': self.toggle_sign,
            '%': self.percent,
            '=': self.equal
        }
        if key in actions:
            actions[key]()
        elif key in ['+', '-', '×', '÷']:
            self.set_operator(key)
        elif key == '.':
            self.append_dot()
        else:
            self.append_number(key)
        self.update_display()

    # 더하기 연산자 처리
    def append_number(self, num):
        if self.operator:
            self.second_number += num
        else:
            self.first_number += num

    # 소수점은 이미 존재하지 않는 경우에만 추가
    def append_dot(self):
        target = self.second_number if self.operator else self.first_number
        if '.' not in target:
            self.append_number('.')

    # 연산자를 설정하고, 이후에 두 번째 숫자를 입력받을 준비
    def set_operator(self, op):
        if self.first_number:
            self.operator = op

    # AC버튼 클릭시 초기화
    def reset(self):
        self.first_number = ''
        self.second_number = ''
        self.operator = ''
        self.result = ''
        self.display.setText('0')

    # +/- 부호 변환 기능
    def toggle_sign(self):
        target = self.second_number if self.operator else self.first_number
        if target:
            if target.startswith('-'):
                target = target[1:]
            else:
                target = '-' + target
            if self.operator:
                self.second_number = target
            else:
                self.first_number = target

    # % 기능
    def percent(self):
        try:
            target = float(self.second_number if self.operator else self.first_number)
            target /= 100
            if self.operator:
                self.second_number = str(target)
            else:
                self.first_number = str(target)
        except:
            self.result = 'Error'
    
    # 덧셈 기능
    def add(self, a, b):
        return a + b
    
    # 뺄셈 기능
    def subtract(self, a, b): 
        return a - b
    
    # 곱셉 기능
    def multiply(self, a, b): 
        return a * b
    
    # 나누기 기능
    def divide(self, a, b):
        if b == 0:      # 0으로 나누는 오류를 방지
            raise ZeroDivisionError # b == 0이면 ZeroDivisionError를 발생
        return a / b

    # 계산 및 결과 출력
    def equal(self):
        try:
            a = float(self.first_number)    # 첫 번째 값
            b = float(self.second_number)   # 두 번째 값
            operations = {
                '+': self.add,
                '-': self.subtract,
                '×': self.multiply,
                '÷': self.divide
            }
            self.result = str(round(operations[self.operator](a, b), 6)) # round 6을 이용해 소수점 6자리로 반올림
            self.first_number = self.result # 계산이 끝난 후, first_number를 계산된 결과(self.result)로 갱신
            self.second_number = '' # 계산이 완료되면 두 번째 숫자 초기화
            self.operator = '' # 연산자도 계산 후 초기화
        
        except ZeroDivisionError:  # 0으로 나누는 경우에 대한 예외 처리
            self.result = 'Error'
        
        except ValueError:  # 숫자 변환이 불가능한 경우 (예: 빈 값)
            self.result = 'Error'

        except Exception as e:  # 그외 모든 예외를 처리
            self.result = 'Error'

    # 결과가 화면에 표시될 때, 글자 크기를 동적으로 조정
    def update_display(self):
        text = self.result or self.second_number or self.first_number or '0' # 디스플레이에 보여줄 텍스트를 결정
        length = len(text)
        font_size = 64 if length < 10 else max(20, 64 - (length - 9) * 4) # text의 길이가 10자 이상이라면, 글자 크기를 자동으로 줄여서 표시
        self.display.setStyleSheet(f"color: white; font-size: {font_size}px; padding: 30px 10px 10px 10px;")
        self.display.setText(text)

# 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec())