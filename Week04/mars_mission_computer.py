import random
from datetime import datetime
import time
import json
import threading

# DummySensor 클래스 정의
class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": 0,
            "mars_base_external_temperature": 0,
            "mars_base_internal_humidity": 0,
            "mars_base_external_illuminance": 0,
            "mars_base_internal_co2": 0,
            "mars_base_internal_oxygen": 0
        }

    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4, 7)

    def get_env(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("./Week04/env_log.txt", "a") as file:
            file.write(f"1. 날짜와 시간: {current_time}\n"
                    f"2. 화성 기지 내부 온도: {self.env_values['mars_base_internal_temperature']:.2f}°C\n"
                    f"3. 화성 기지 외부 온도: {self.env_values['mars_base_external_temperature']:.2f}°C\n"
                    f"4. 화성 기지 내부 습도: {self.env_values['mars_base_internal_humidity']:.2f}%\n"
                    f"5. 화성 기지 외부 광량: {self.env_values['mars_base_external_illuminance']:.2f} W/m²\n"
                    f"6. 화성 기지 내부 이산화탄소 농도: {self.env_values['mars_base_internal_co2']:.2f}%\n"
                    f"7. 화성 기지 내부 산소 농도: {self.env_values['mars_base_internal_oxygen']:.2f}%\n\n")
        return {key: round(value, 2) for key, value in self.env_values.items()}

# ds라는 이름으로 인스턴스화
ds = DummySensor()

class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.sensor = ds
        self.running = True
        self.data_log = []

    def get_sensor_data(self):
        def input_thread():
            input("\n종료하려면 Enter 키를 누르세요...\n")
            self.running = False

        threading.Thread(target=input_thread).start()
        start_time = time.time()

        while self.running:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

            self.data_log.append(self.env_values.copy())
            
            if len(self.data_log) >= 60:  # 5분(60초) 동안 5초마다 1번씩 = 60개
                avg_data = {}
                for key in self.data_log[0].keys():
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

            time.sleep(5)

        print("System stopped...")

# RunComputer 인스턴스 생성 및 실행
RunComputer = MissionComputer()
RunComputer.get_sensor_data()
