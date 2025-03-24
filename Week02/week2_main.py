import csv
import os
import struct
# CSV 파일 읽고 리스트 변환
def read_csv_to_list(filename):
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)    # 헤더 저장
            print("원본 CSV 파일 헤더:", headers)    # 헤더 출력
            for row in reader:
                try:
                    # 인화성 지수 변환 (없거나 "Various"이면 0으로 처리)
                    flammability = float(row[4]) if row[4].replace('.', '', 1).isdigit() else 0
                    data.append([row[0], row[1], row[2], row[3], flammability])  
                except ValueError:
                    continue    # 데이터 오류 시 무시
        print("원본 CSV 파일 내용 출력:")
        for row in data:
            print(row)
    except FileNotFoundError:
        print(f"파일 {filename}을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    return data

# 인화성이 높은 순으로 정렬
def sort_by_flammability(data):
    return sorted(data, key=lambda x: x[4], reverse=True)

# 인화성 지수 0.7 이상 필터링
def filter_high_flammability(data, threshold=0.7):
    return [row for row in data if row[4] >= threshold]

# CSV 저장
def save_to_csv(filename, data):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Substance", "Weight (g/cm³)", "Specific Gravity", "Strength", "Flammability"])
            writer.writerows(data)
    except Exception as e:
        print(f"CSV 저장 오류: {e}")

# ✅ 이진 파일 저장 (진짜 struct 이진 저장 방식)
def save_to_binary(filename, data):
    try:
        with open(filename, "wb") as file:
            for row in data:
                # 각 문자열 필드는 고정 길이로 맞춰 자름 + 공백으로 채움
                substance = row[0][:20].ljust(20)
                weight = row[1][:10].ljust(10)
                gravity = row[2][:10].ljust(10)
                strength = row[3][:10].ljust(10)
                flammability = row[4]

                packed = struct.pack(
                    "20s10s10s10sf",
                    substance.encode("utf-8"),
                    weight.encode("utf-8"),
                    gravity.encode("utf-8"),
                    strength.encode("utf-8"),
                    flammability
                )
                file.write(packed)
    except Exception as e:
        print(f"이진 파일 저장 오류: {e}")

# ✅ 이진 파일 읽기 (struct 언패킹으로 정확히 읽기)
def read_from_binary(filename):
    try:
        with open(filename, "rb") as file:
            record_size = struct.calcsize("20s10s10s10sf")  # 한 레코드 크기 계산
            print("\n이진 파일 내용 출력:")
            while True:
                chunk = file.read(record_size)
                if not chunk:
                    break
                unpacked = struct.unpack("20s10s10s10sf", chunk)
                decoded = [field.decode("utf-8").strip() if isinstance(field, bytes) else field for field in unpacked]
                print(decoded)
    except Exception as e:
        print(f"이진 파일 읽기 오류: {e}")

# 파일 경로 (윈도우에서는 r"" 또는 \\ 사용)
csv_filename = r"C:\Codessey\Week02\Mars_Base_Inventory_List.csv"
binary_filename = r"C:\Codessey\Week02\Mars_Base_Inventory_List.bin"
dangerous_csv_filename = r"C:\Codessey\Week02\Mars_Base_Inventory_danger.csv"

# 실행
inventory_data = read_csv_to_list(csv_filename)
sorted_data = sort_by_flammability(inventory_data)
dangerous_materials = filter_high_flammability(sorted_data)

save_to_csv(csv_filename, sorted_data)
save_to_csv(dangerous_csv_filename, dangerous_materials)

save_to_binary(binary_filename, sorted_data)
read_from_binary(binary_filename)