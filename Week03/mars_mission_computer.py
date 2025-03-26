import random
from datetime import datetime

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
        with open("C:\Codessey\Week03\env_log.txt", "a") as file:
            file.write(f"1. 날짜와 시간: {current_time}\n"
            f"2. 화성 기지 내부 온도: {self.env_values['mars_base_internal_temperature']:.2f}°C\n"
            f"3. 화성 기지 외부 온도: {self.env_values['mars_base_external_temperature']:.2f}°C\n"
            f"4. 화성 기지 내부 습도: {self.env_values['mars_base_internal_humidity']:.2f}%\n"
            f"5. 화성 기지 외부 광량: {self.env_values['mars_base_external_illuminance']:.2f} W/m²\n"
            f"6. 화성 기지 내부 이산화탄소 농도: {self.env_values['mars_base_internal_co2']:.2f}%\n"
            f"7. 화성 기지 내부 산소 농도: {self.env_values['mars_base_internal_oxygen']:.2f}%\n\n")

        # 소수점 두 자릿수로 값을 제한하여 터미널창에 출력
        return {key: round(value, 2) for key, value in self.env_values.items()}


# 인스턴스화 및 실행
ds = DummySensor()

# 환경 변수 설정
ds.set_env()

# 환경 변수 출력 및 로그 기록
env_data = ds.get_env()
print(env_data)
