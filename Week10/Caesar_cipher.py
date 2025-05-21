import os

def caesar_cipher_decode(target_text):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    for shift in range(1, 26):
        decrypted = ''
        for char in target_text:
            if char.isalpha():
                lower_char = char.lower()
                index = (alphabet.index(lower_char) - shift) % 26
                new_char = alphabet[index]
                decrypted += new_char.upper() if char.isupper() else new_char
            else:
                decrypted += char

        print(f"[{shift}] {decrypted}")

    try:
        selected = int(input("\n올바른 복호화 결과의 번호를 입력하세요 (1~25): "))
        if 1 <= selected <= 25:
            final_result = ''
            for char in target_text:
                if char.isalpha():
                    lower_char = char.lower()
                    index = (alphabet.index(lower_char) - selected) % 26
                    new_char = alphabet[index]
                    final_result += new_char.upper() if char.isupper() else new_char
                else:
                    final_result += char

            result_path = r'C:\Codessey\Week10\result.txt'  # 저장 경로 지정
            with open(result_path, 'w') as f:
                f.write(final_result)
            print(f"\n✅ result.txt 파일로 저장 완료: {final_result}")
        else:
            print("❌ 유효하지 않은 번호입니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


# password.txt 경로 명확히 지정
password_path = r'C:\Codessey\Week10\password.txt'

try:
    with open(password_path, 'r') as file:
        password = file.read().strip()
        print(f"🔐 복호화할 텍스트: {password}")
        caesar_cipher_decode(password)
except FileNotFoundError:
    print("❌ password.txt 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"❌ 파일을 여는 중 오류 발생: {e}")
