import os
import datetime
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import csv


# 🔴 음성 녹음 함수
def record_voice(duration=5, sample_rate=44100):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_name = os.path.join(base_dir, 'records')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d-%H%M%S")
    wav_path = os.path.join(folder_name, filename + ".wav")

    try:
        print("🎙️ 녹음 시작... 말하세요!")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        wav.write(wav_path, sample_rate, recording)
        print(f"✅ 녹음 완료! 파일 저장 위치: {wav_path}")
    except Exception as e:
        print(f"❌ 녹음 중 오류 발생: {e}")

# 🔴 STT 변환 함수
def convert_speech_to_text(wav_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"📝 인식된 텍스트: {text}")

            csv_path = wav_path.replace(".wav", ".csv")
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'Text'])
                writer.writerow(['00:00', text])
            print(f"✅ CSV 파일 저장 완료: {csv_path}")
    except sr.UnknownValueError:
        print("❌ 음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"❌ STT 요청 오류: {e}")
    except Exception as e:
        print(f"❌ 변환 오류: {e}")

# 🔴 키워드 검색 함수
def search_keyword_in_csv(keyword):
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'records')
    found = False
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            path = os.path.join(folder, file)
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 스킵
                for row in reader:
                    if keyword in row[1]:
                        print(f"🔍 [{file}] {row[0]} - {row[1]}")
                        found = True
    if not found:
        print("⚠️ 키워드가 포함된 결과를 찾을 수 없습니다.")

# 🔴 날짜 범위로 녹음 파일 조회
def list_files_by_date(start_date_str, end_date_str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_name = os.path.join(base_dir, 'records')

    if not os.path.exists(folder_name):
        print("❌ 'records' 폴더가 존재하지 않습니다.")
        return

    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y%m%d")

        print(f"📂 {start_date_str} ~ {end_date_str} 사이 녹음 파일:")
        for file in os.listdir(folder_name):
            if file.endswith(".wav"):
                date_part = file.split('-')[0]
                file_date = datetime.datetime.strptime(date_part, "%Y%m%d")
                if start_date <= file_date <= end_date:
                    print(f"🟢 {file}")
    except ValueError:
        print("❌ 날짜 형식이 잘못되었습니다. (예: 20240601)")

# 🔴 메인 메뉴
if __name__ == "__main__":
    while True:
        print("\n🧠 자비스 기능 메뉴")
        print("1. 🎙️ 음성 녹음")
        print("2. 📁 녹음 파일 날짜별 조회")
        print("3. 🗣️ 음성 파일 STT 변환 (텍스트로 저장)")
        print("4. 🔎 키워드 검색")
        print("5. ❌ 종료")

        choice = input("👉 원하시는 작업 번호를 입력하세요: ").strip()

        if choice == '1':
            try:
                duration = int(input("⏱️ 녹음 시간(초)을 입력하세요: ").strip())
                record_voice(duration)
            except ValueError:
                print("❌ 숫자로 입력해주세요.")
        elif choice == '2':
            start = input("🔹 시작 날짜를 입력하세요 (예: 20240601): ").strip()
            end = input("🔹 종료 날짜를 입력하세요 (예: 20240610): ").strip()
            list_files_by_date(start, end)
        elif choice == '3':
            filename = input("📄 변환할 .wav 파일명을 입력하세요 (예: 20240601-153000.wav): ").strip()
            folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'records')
            full_path = os.path.join(folder, filename)
            if os.path.exists(full_path):
                convert_speech_to_text(full_path)
            else:
                print("❌ 해당 파일이 존재하지 않습니다.")
        elif choice == '4':
            keyword = input("🔍 검색할 키워드를 입력하세요: ").strip()
            search_keyword_in_csv(keyword)
        elif choice == '5':
            print("👋 자비스를 종료합니다.")
            break
        else:
            print("❌ 유효하지 않은 입력입니다. 1~5 중에서 선택해주세요.")
