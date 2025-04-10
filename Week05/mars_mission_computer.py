import os            # 운영체제 정보를 다루는 기본 모듈 (명령어 실행, 코어 수 등)
import platform      # OS, CPU, 아키텍처 등의 정보를 가져오는 모듈
import json          # 데이터를 JSON 형식으로 보기 좋게 출력하기 위한 모듈

class MissionComputer:
    # 생성자: 클래스가 생성될 때 setting.txt 파일에서 설정을 읽어온다
    def __init__(self, config_file="./Week05/setting.txt"):
        self.config = self.load_config(config_file)  # 설정 정보를 딕셔너리로 저장

    # 설정 파일을 읽어서 출력할 항목이 어떤 것인지 저장하는 함수
    def load_config(self, config_file):
        config = {}
        try:
            with open(config_file, "r") as file:
                for line in file:
                    key, value = line.strip().split("=")
                    config[key.strip()] = value.strip().lower() == 'true'
        except Exception as e:
            print(f"Error loading config file: {e}")  # 파일이 없거나 포맷이 이상할 경우 에러 출력
        return config

    # 시스템 기본 정보 출력 함수 (운영체제, CPU, 메모리 등)
    def get_mission_computer_info(self):
        try:
            system_info = {}

            # 사용자가 'setting.txt'파일에서 True로 설정한 항목만 출력
            if self.config.get("os_name", False):
                system_info['os_name'] = platform.system() # 운영체제 이름
            if self.config.get("os_version", False):
                system_info['os_version'] = platform.version() # 운영체제 버전
            if self.config.get("cpu_type", False):
                system_info['cpu_type'] = platform.processor() # CPU 종류(모델명)
            if self.config.get("cpu_cores", False):
                system_info['cpu_cores'] = os.cpu_count() # CPU 코어 수 가져오기

            # 메모리 크기 (Windows 기준): wmic 명령어를 사용해서 각 메모리 칩의 용량을 모두 더한다
            if self.config.get("memory", False): # 'setting.txt'파일에서 True로 설정시 실행, False이면 이 블록 전체를 건너뜀
                if platform.system() == "Windows":
                    memory_info = os.popen("wmic MemoryChip get Capacity").readlines() # Windows 명령어 실행
                    total_memory = sum(
                        int(line.strip()) for line in memory_info[1:] if line.strip().isdigit() # 두 번째 줄부터 숫자인 줄만 걸러 정수 변환 후 모두 더함
                    )
                    system_info['memory'] = round(total_memory / (1024 ** 3), 2)  # B 부터 GB로 변환하기 위해 1024^3으로 나눔, round(..., 2)는 소수점 2자리까지 반올림
                else:
                    system_info['memory'] = "운영체제를 확인하세요!" # 지원하지 않는 운영체제

            # JSON 형식으로 보기 좋게 출력
            print(json.dumps(system_info, indent=4))
            return system_info

        except Exception as e:
            print(f"Error while fetching system info: {e}")
            return None

    # 실시간 시스템 부하 정보를 출력하는 함수 (CPU, 메모리 사용률)
    def get_mission_computer_load(self):
        try:
            load_info = {}

            # CPU 사용률 가져오기 (Windows 전용)
            if self.config.get("cpu_usage", False): # 'setting.txt'파일에서 True로 설정시 실행, False이면 이 블록 전체를 건너뜀
                if platform.system() == "Windows":
                    cpu_output = os.popen("wmic cpu get loadpercentage").readlines() # Windows 명령어 실행
                    cpu_lines = [line.strip() for line in cpu_output if line.strip()] # 빈 줄 제거하고 strip()한 값만 남김
                    load_info['cpu_usage'] = cpu_lines[1] if len(cpu_lines) >= 2 else "Error" # 첫 줄은 헤더, 두 번째 줄이 실제 사용률
                else:
                    load_info['cpu_usage'] = "운영체제를 확인하세요!" # 지원하지 않는 운영체제

            # 메모리 사용률 가져오기
            if self.config.get("memory_usage", False): # 'setting.txt'파일에서 True로 설정시 실행, False이면 이 블록 전체를 건너뜀
                if platform.system() == "Windows":
                    mem_output = os.popen("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize").readlines() # Windows 명령어 실행
                    mem_lines = [line.strip() for line in mem_output if line.strip()]
                    if len(mem_lines) >= 2: # 두 번째 줄에 실제 값이 있음: [FreePhysicalMemory(사용가능 메모리), TotalVisibleMemorySize(전체 메모리)]
                        parts = mem_lines[1].split()
                        if len(parts) >= 2:
                            TotalVisibleMemorySize = int(parts[1]) / 1024   # KB → MB 변환하기 위해 1024으로 나눔
                            FreePhysicalMemory = int(parts[0]) / 1024
                            used_percent = ((TotalVisibleMemorySize - FreePhysicalMemory) / TotalVisibleMemorySize) * 100
                            load_info['memory_usage'] = round(used_percent, 2)  # 소수점 2자리 반올림
                        else:
                            load_info['memory_usage'] = "Parsing error" # 숫자 2개가 없으면 파싱 에러로 처리
                    else:
                        load_info['memory_usage'] = "Fetch error" # 값을 가져올 때 오류
                else:
                    load_info['memory_usage'] = "운영체제를 확인하세요!" # 지원하지 않는 운영체제

            # 부하 정보도 JSON 형식으로 출력
            print(json.dumps(load_info, indent=4))
            return load_info

        except Exception as e:
            print(f"Error while fetching system load: {e}")
            return None


# ▶︎ 클래스 인스턴스를 만들어 실제 동작하게 함
runComputer = MissionComputer()
runComputer.get_mission_computer_info()   # 시스템 기본 정보 출력
runComputer.get_mission_computer_load()   # 실시간 부하 정보 출력
