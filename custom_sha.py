'''import struct
import sys, io
'''
# UTF-8対応
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 初期ハッシュ値
INITIAL_HASH = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

# 定数K
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c
]

# 右回転関数
def right_rotate(value, bits):
    return ((value >> bits) | (value << (32 - bits))) & 0xFFFFFFFF

# カスタムSHA-256メイン関数
def tocustom_sha256(number_str):
    # 23桁の整数チェック
    if not (len(number_str) == 23 and number_str.isdigit()):
        raise ValueError("Input must be a 23-digit integer string.")

    # 2進数に変換し、32ビット×3行のMessage Blockに分割
    binary_message = f"{int(number_str):077b}"

    # メッセージの最後に1を追加
    binary_message += '1'

    # 入力の長さを3行目の最後に付加
    message_length = len(number_str) * 4
    binary_message = binary_message.ljust(96 - 8, '0') + f"{message_length:08b}"

    # Message Blockに変換
    w = [int(binary_message[i:i + 32], 2) for i in range(0, 96, 32)]

    # Message Scheduleを51行に拡張
    w += [0] * (51 - len(w))
    for i in range(3, 51):
        s0 = right_rotate(w[i - 3], 7) ^ right_rotate(w[i - 3], 18) ^ (w[i - 3] >> 3)
        s1 = right_rotate(w[i - 1], 17) ^ right_rotate(w[i - 1], 19) ^ (w[i - 1] >> 10)
        w[i] = (w[i - 3] + s0 + w[i - 2] + s1) & 0xFFFFFFFF

    # 初期ハッシュ値のコピー
    a, b, c, d, e, f, g, h = INITIAL_HASH

    # 圧縮関数の実行
    for i in range(51):
        s1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
        ch = (e & f) ^ (~e & g)
        temp1 = (h + s1 + ch + K[i] + w[i]) & 0xFFFFFFFF
        s0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (s0 + maj) & 0xFFFFFFFF

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF

    # ハッシュ値の計算
    hash_pieces = [(x + y) & 0xFFFFFFFF for x, y in zip(INITIAL_HASH, [a, b, c, d, e, f, g, h])]

    return ''.join(f'{piece:08x}' for piece in hash_pieces)


# テスト
if __name__ == "__main__":
    test_number = "00009876876536473627364"
    print(f"Custom SHA-256({test_number}) = {tocustom_sha256(test_number)}")

