import random
from datetime import datetime
import time
import json
import threading

# DummySensor 클래스 정의
class DummySensor:
    def __init__(self): #초기화 메소드 (특수 메소드, 파이썬 내장 메소드)
        # 클래스 인스턴스가 생성될 때 자동으로 호출
        # 초기화 작업: env_values 딕셔너리 객체 정의
        self.env_values = {
            "mars_base_internal_temperature": 0,
            "mars_base_external_temperature": 0,
            "mars_base_internal_humidity": 0,
            "mars_base_external_illuminance": 0,
            "mars_base_internal_co2": 0,
            "mars_base_internal_oxygen": 0
        }

    def set_env(self):
        # 각 환경 변수에 랜덤 값 할당
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)  # 18~30도 랜덤 생성
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)  # 0~21도 랜덤 생성
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)  # 50~60% 랜덤 생성
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)  # 500~715 W/m² 랜덤 생성
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)  # 0.02~0.1% 랜덤 생성
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4, 7)  # 4%~7% 랜덤 생성

    def get_env(self):
        # 현재 날짜와 시간을 가져와서 포맷
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 로그 파일에 기록 (날짜, 시간 포함, 항목 이름과 값)
        with open("./Week04/env_log.txt", "a") as file:
            file.write(f"1. 날짜와 시간: {current_time}\n"
                f"2. 화성 기지 내부 온도: {self.env_values['mars_base_internal_temperature']:.2f}°C\n"
                f"3. 화성 기지 외부 온도: {self.env_values['mars_base_external_temperature']:.2f}°C\n"
                f"4. 화성 기지 내부 습도: {self.env_values['mars_base_internal_humidity']:.2f}%\n"
                f"5. 화성 기지 외부 광량: {self.env_values['mars_base_external_illuminance']:.2f} W/m²\n"
                f"6. 화성 기지 내부 이산화탄소 농도: {self.env_values['mars_base_internal_co2']:.2f}%\n"
                f"7. 화성 기지 내부 산소 농도: {self.env_values['mars_base_internal_oxygen']:.2f}%\n\n")
        # 소수점 두 자릿수로 값을 제한하여 터미널창에 출력
        return {key: round(value, 2) for key, value in self.env_values.items()}

# ds라는 이름으로 인스턴스화
ds = DummySensor()

class MissionComputer:
    def __init__(self):
        self.env_values = {}          # 현재 센서 데이터를 담을 딕셔너리
        self.sensor = ds              # DummySensor 인스턴스를 사용
        self.running = True           # 센서 루프 실행 여부를 제어하는 변수
        self.data_log = []            # 5분 동안 측정한 데이터를 저장하는 리스트

    def get_sensor_data(self):
        # 사용자 입력(Enter 키)을 감지하는 별도 스레드 시작
        def input_thread():
            input("\n종료하려면 Enter 키를 누르세요...\n")
            self.running = False    # Enter 입력 시 루프 종료

        threading.Thread(target=input_thread).start()   # 스레드 실행
        
        # 센서 측정을 반복하는 루프
        while self.running:
            self.sensor.set_env()   # 랜덤 환경값 생성
            self.env_values = self.sensor.get_env() # 환경값을 가져옴
            print(json.dumps(self.env_values, indent=4, ensure_ascii=False))
            
            #self.data_log 리스트에 수집한 값을 계속 추가
            self.data_log.append(self.env_values.copy())
            
            if len(self.data_log) >= 60:  # 5분(60초) 동안 5초마다 1번씩 = 60개
                avg_data = {}
                for key in self.data_log[0].keys():
                    # 각 항목별 평균값 계산
                    avg_data[key] = round(sum(d[key] for d in self.data_log) / len(self.data_log), 2)
                    
                print("\n[5분 평균값 출력]")
                print(json.dumps(avg_data, indent=4, ensure_ascii=False))
                
                # 평균값을 env_log.txt에도 저장
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("./Week04/env_log.txt", "a") as file:
                    file.write(f"[------------5분 평균값------------]\n"
                            f"1. 날짜와 시간: {current_time}\n"
                            f"2. 화성 기지 내부 온도: {avg_data['mars_base_internal_temperature']:.2f}°C\n"
                            f"3. 화성 기지 외부 온도: {avg_data['mars_base_external_temperature']:.2f}°C\n"
                            f"4. 화성 기지 내부 습도: {avg_data['mars_base_internal_humidity']:.2f}%\n"
                            f"5. 화성 기지 외부 광량: {avg_data['mars_base_external_illuminance']:.2f} W/m²\n"
                            f"6. 화성 기지 내부 이산화탄소 농도: {avg_data['mars_base_internal_co2']:.2f}%\n"
                            f"7. 화성 기지 내부 산소 농도: {avg_data['mars_base_internal_oxygen']:.2f}%\n\n")
                
                self.data_log = []  # 초기화하여 다음 5분 측정 준비
            
            #5초마다 센서 데이터 수집
            time.sleep(5)

        print("System stopped...")

# RunComputer 인스턴스 생성 및 실행
RunComputer = MissionComputer()
RunComputer.get_sensor_data()
