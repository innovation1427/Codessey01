import os
import datetime
import sounddevice as sd
import scipy.io.wavfile as wav

# 🎙️ 녹음 함수
def record_voice(sample_rate=44100):
    try:
        duration = int(input("⏱️ 녹음 시간(초)을 입력하세요: ").strip())
    except ValueError:
        print("❌ 숫자만 입력해주세요.")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_name = os.path.join(base_dir, 'records')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d-%H%M%S") + ".wav"
    filepath = os.path.join(folder_name, filename)

    try:
        print("🎙️ 녹음 시작... 말하세요!")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        wav.write(filepath, sample_rate, recording)
        print(f"✅ 녹음 완료! 파일 저장 위치: {filepath}")
    except Exception as e:
        print(f"❌ 녹음 중 오류 발생: {e}")


# 📁 녹음 파일 날짜 조회 함수
def list_files_by_date(start_date_str, end_date_str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_name = os.path.join(base_dir, 'records')

    if not os.path.exists(folder_name):
        print("❌ 'records' 폴더가 존재하지 않습니다.")
        return

    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y%m%d")

        print(f"\n📂 {start_date_str} ~ {end_date_str} 사이 녹음 파일:")
        found = False
        for file in os.listdir(folder_name):
            if file.endswith(".wav"):
                file_date_str = file.split('-')[0]
                file_date = datetime.datetime.strptime(file_date_str, "%Y%m%d")
                if start_date <= file_date <= end_date:
                    print(f"🟢 {file}")
                    found = True
        if not found:
            print("⚠️ 해당 범위에 녹음된 파일이 없습니다.")
    except ValueError:
        print("❌ 날짜 형식이 잘못되었습니다. (예: 20240601)")


# 🔧 메인 메뉴
if __name__ == "__main__":
    while True:
        print("\n🧠 자비스 기능 메뉴")
        print("1. 🎙️ 음성 녹음")
        print("2. 📁 녹음 파일 날짜별 조회")
        print("3. ❌ 종료")

        choice = input("👉 원하시는 작업 번호를 입력하세요: ").strip()

        if choice == '1':
            record_voice()
        elif choice == '2':
            start = input("🔹 시작 날짜를 입력하세요 (예: 20240601): ").strip()
            end = input("🔹 종료 날짜를 입력하세요 (예: 20240610): ").strip()
            list_files_by_date(start, end)
        elif choice == '3':
            print("👋 자비스를 종료합니다.")
            break
        else:
            print("❌ 유효하지 않은 입력입니다. 1, 2, 3 중에서 선택해주세요.")
            