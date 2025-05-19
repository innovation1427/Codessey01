import zipfile
import itertools
import string
import time
import zlib

def unlock_zip():
    # 시작 시간 기록
    start_time = time.time()

    # ✅ 경로 수정 (raw string format 사용)
    zip_file = r'C:\Codessey\Week09\emergency_storage_key.zip'
    password_file = r'C:\Codessey\Week09\password.txt'
    
    # 가능한 문자들: 숫자(0-9) + 소문자 알파벳(a-z)
    characters = string.ascii_lowercase + string.digits
    total_combinations = len(characters) ** 6  # 총 조합 수 계산

    print(f"총 {total_combinations} 개의 조합을 시도합니다.")

    # zip 파일을 엽니다.
    with zipfile.ZipFile(zip_file, 'r') as zf:
        # 가능한 모든 6자리 조합을 생성하여 순차적으로 시도
        for i, password_tuple in enumerate(itertools.product(characters, repeat=6)):
            password = ''.join(password_tuple)
            
            # 비밀번호 시도
            try:
                # 🔍 **암호가 맞는지 확인**
                if zf.testzip() is None:
                    zf.extractall(path='.', pwd=password.encode())  # 비밀번호를 사용하여 파일 추출
                    print(f"🔓 비밀번호 찾음! 비밀번호는: {password}")
                    
                    # 비밀번호를 파일에 저장
                    with open(password_file, 'w') as pw_file:
                        pw_file.write(password)
                    
                    # 종료 시간 기록
                    end_time = time.time()
                    print(f"⏰ 시작 시간: {start_time}")
                    print(f"⏳ 진행 시간: {end_time - start_time:.2f}초")
                    print(f"🔎 반복 횟수: {i+1}/{total_combinations}")
                    break  # 비밀번호를 찾으면 종료
                
            except (RuntimeError, zipfile.BadZipFile):
                if i % 1000 == 0:  # 1000번 시도마다 진행상황 출력
                    print(f"⏳ 진행 중... {i+1}/{total_combinations}")
                continue
            except zlib.error as e:
                print(f"❌ 압축 해제 중 에러 발생: {e}")
                continue
        else:
            print("❌ 암호를 찾을 수 없습니다.")

if __name__ == "__main__":
    unlock_zip()
