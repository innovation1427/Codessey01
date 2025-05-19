import zipfile
import itertools
import string
import time
import zlib
import contextlib
import multiprocessing

def try_password_range(start, end, zip_file, password_file, characters, progress_list):
    # zip 파일을 엽니다.
    with zipfile.ZipFile(zip_file, 'r') as zf:
        for i, password_tuple in enumerate(itertools.islice(itertools.product(characters, repeat=6), start, end)):
            password = ''.join(password_tuple)
            
            try:
                # ⚠️ 에러 로그를 숨기기 위해 contextlib 사용
                with contextlib.redirect_stderr(None):
                    zf.extractall(path='.', pwd=password.encode())  # 비밀번호를 사용하여 파일 추출

                # 비밀번호를 찾은 경우
                print(f"\n🔓 비밀번호 찾음! 비밀번호는: {password}")
                
                # 비밀번호를 파일에 저장
                with open(password_file, 'w') as pw_file:
                    pw_file.write(password)
                
                return password  # 비밀번호 찾았으므로 종료
            except (RuntimeError, zipfile.BadZipFile):
                continue
            except zlib.error:
                continue
            
            # 진행상황을 부모 프로세스로 전달
            progress_list.append(i + start)
    return None  # 비밀번호를 찾지 못한 경우

def unlock_zip():
    # 시작 시간 기록
    start_time = time.time()

    # 경로 수정 (raw string format 사용)
    zip_file = r'C:\Codessey\Week09\emergency_storage_key.zip'  # zip 파일 경로
    password_file = r'C:\Codessey\Week09\password.txt'  # 비밀번호 저장 파일
    
    # 가능한 문자들: 숫자(0-9) + 소문자 알파벳(a-z)
    characters = string.ascii_lowercase + string.digits
    total_combinations = len(characters) ** 6  # 총 조합 수 계산 (36^6)

    print(f"총 {total_combinations:,} 개의 조합을 시도합니다.")

    # 프로세스 수 설정
    num_processes = multiprocessing.cpu_count()  # CPU 코어 수만큼 프로세스 생성
    
    # 멀티프로세스를 위한 Manager 객체 생성
    with multiprocessing.Manager() as manager:
        progress_list = manager.list()  # 공유 가능한 리스트로 진행 상태 저장

        # 각 프로세스가 처리할 범위 계산
        chunk_size = total_combinations // num_processes
        ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
        
        # 마지막 프로세스는 남은 범위까지 처리
        ranges[-1] = (ranges[-1][0], total_combinations)
        
        # 멀티프로세스로 비밀번호 시도
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.starmap(try_password_range, [(start, end, zip_file, password_file, characters, progress_list) for start, end in ranges])

        # 진행 상태 출력
        def print_progress():
            processed = 0
            while processed < total_combinations:
                if len(progress_list) > processed:
                    processed = len(progress_list)
                    print(f"\r⏳ 진행 중... {processed:,}/{total_combinations:,} 시도", end="")
        
        # 진행 상태 출력 프로세스 시작
        progress_process = multiprocessing.Process(target=print_progress)
        progress_process.start()

        # 비밀번호를 찾았는지 확인
        for result in results:
            if result:
                end_time = time.time()
                print(f"\n⏰ 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
                print(f"⏳ 진행 시간: {end_time - start_time:.2f}초")
                break
        else:
            print("\n암호를 찾을 수 없습니다.")

        # 진행 상태 출력 프로세스 종료
        progress_process.terminate()

if __name__ == "__main__":
    unlock_zip()