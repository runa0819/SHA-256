# import hashlib
import json
import datetime
import sha256

# ファイルに保存するためのログリスト
log_file = "entry_exit_logs.json"

def hash_data(student_id, action, timestamp):
    """
    学生番号、タイムスタンプ、アクションを結合し、SHA-256でハッシュ化する
    """
    data = f"{student_id}{action}{timestamp}"
    return sha256.tosha256(data)

def save_log(student_id, action):
    """
    学生番号とアクション（入室/退室）をログに保存する
    """
    timestamp = datetime.datetime.now().isoformat()
    hashed = hash_data(student_id, action, timestamp)

    log_entry = {
        "student_id": student_id,
        "action": action,
        "timestamp": timestamp,
        "hash": hashed
    }

    # ファイルにログを追加
    try:
        with open(log_file, "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)

    with open(log_file, "w") as file:
        json.dump(logs, file, indent=4)

    print("ログを保存しました:", log_entry)

def display_logs():
    """
    保存されたログを表示する
    """
    try:
        with open(log_file, "r") as file:
            logs = json.load(file)
            if len(logs) == 0 :
                print("ログが存在しません。")
            for log in logs:
                print(log)
    except FileNotFoundError:
        print("ログファイルが存在しません。")

def calculate_merkle_root():
    """
    ログファイル内のハッシュ値を使用してマークルツリーのルートハッシュを計算する
    """
    try:
        with open(log_file, "r") as file:
            logs = json.load(file)
            hashes = [log["hash"] for log in logs]

        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                # 奇数の場合、最後の要素を繰り返す
                hashes.append(hashes[-1])

            # ハッシュペアを結合して新しいハッシュリストを作成
            hashes = [
                sha256.tosha256((hashes[i] + hashes[i + 1]))
                for i in range(0, len(hashes), 2)
            ]

        return hashes[0] if hashes else None

    except FileNotFoundError:
        print("ログファイルが存在しません。")
        return None

def clear_logs():
    """
    ログファイルをクリアにする
    """
    with open(log_file, "w") as file:
        json.dump([], file)
    print("ログファイルをクリアしました。")
 

if __name__ == "__main__":
    while True:
        print("\n1: 入室記録\n2: 退室記録\n3: ログ表示\n4: ルートハッシュ計算\n5: ログクリア\n6: 終了")
        choice = input("選択してください: ")

        if choice == "1":
            student_id = input("学生番号を入力してください（9桁）: ")
            if len(student_id) == 9 and student_id.isdigit():
                save_log(student_id, "entry")
            else:
                print("無効な学生番号です。9桁の数字を入力してください。")
        elif choice == "2":
            student_id = input("学生番号を入力してください（9桁）: ")
            if len(student_id) == 9 and student_id.isdigit():
                save_log(student_id, "exit")
            else:
                print("無効な学生番号です。9桁の数字を入力してください。")
        elif choice == "3":
            display_logs()
        elif choice == "4":
            root_hash = calculate_merkle_root()
            if root_hash:
                print("ルートハッシュ:", root_hash)
            else:
                print("ルートハッシュを計算できませんでした。")
        elif choice == "5":
            clear_logs()
        elif choice == "6":
            print("プログラムを終了します。")
            break
        else:
            print("無効な選択です。")
        print("------------------------------------------")
