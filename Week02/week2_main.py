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
        print("원본 CSV 파일 내용 출력:")    # CSV 내용 일부 출력
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

# 이진 파일 저장
def save_to_binary(filename, data):
    try:
        with open(filename, "wb") as file:
            for row in data:
                line = ",".join(str(item) for item in row) + "\n"
                file.write(line.encode("utf-8"))  # UTF-8로 인코딩하여 저장
    except Exception as e:
        print(f"이진 파일 저장 오류: {e}")


# 이진 파일 읽기
def read_from_binary(filename):
    try:
        with open(filename, "rb") as file:
            content = file.read().decode("utf-8")  # UTF-8로 디코딩하여 읽기
            print(content)
    except Exception as e:
        print(f"이진 파일 읽기 오류: {e}")


# 실행 과정
csv_filename = "C:\Codessey\Week02\Mars_Base_Inventory_List.csv"
binary_filename = "C:\Codessey\Week02\Mars_Base_Inventory_List.bin"
dangerous_csv_filename = "C:\Codessey\Week02\Mars_Base_Inventory_danger.csv"

# CSV 읽기 및 리스트 변환
inventory_data = read_csv_to_list(csv_filename)

# 인화성 지수 기준 정렬
sorted_data = sort_by_flammability(inventory_data)

# 0.7 이상 필터링
dangerous_materials = filter_high_flammability(sorted_data)

# 정렬된 데이터 CSV 저장
save_to_csv(csv_filename, sorted_data)

# 위험 물질 CSV 저장
save_to_csv(dangerous_csv_filename, dangerous_materials)

# 정렬된 데이터 이진 파일 저장
save_to_binary(binary_filename, sorted_data)

# 저장된 이진 파일 읽기
print("\n 이진 파일 내용 출력:")
read_from_binary(binary_filename)
