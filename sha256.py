import struct
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#UTF-8に対応させる

# 初期ハッシュ値と定数の設定
INITIAL_HASH = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

#3乗根の小数点以下
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


# 右回転の関数
#ROTR関数循環シフト
def right_rotate(value, bits):
    return ((value >> bits) | (value << (32 - bits))) & 0xFFFFFFFF

# メインのSHA-256計算関数
def tosha256(message):
    # メッセージのパディング
    #バイトレベルで操作可能
    message = bytearray(message, encoding='utf-8')
    #入力の長さを最後に付加する必要があるため保持
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    #入力の最後に1を追加する(0x80:10000000)
    message.append(0x80)
    #入力の最後に1を追加したブロック～入力の長さを追加するブロックまで0を入力
    while len(message) % 64 != 56:
        message.append(0)
    #最後のブロックにはデータの長さを入れる
    message += orig_len_in_bits.to_bytes(8, byteorder='big')
    #ここでMessage Blockの完成

    # ハッシュの初期化
    hash_pieces = INITIAL_HASH[:]

    # 512ビットずつメッセージを処理
    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        w = list(struct.unpack('>16L', chunk)) + [0] * 48

        #Message Scheduleを作成
        for i in range(16, 64):
            #(w[i]>>x)x個ずらす、あふれた分は切り捨て
            s0 = (right_rotate(w[i - 15], 7) ^ right_rotate(w[i - 15], 18) ^ (w[i - 15] >> 3))
            s1 = (right_rotate(w[i - 2], 17) ^ right_rotate(w[i - 2], 19) ^ (w[i - 2] >> 10))
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = hash_pieces

        # 圧縮関数
        for i in range(64):
            #Σ1関数
            s1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            #choose関数(e = 1:f,e != 1:g)
            ch = (e & f) ^ (~e & g)
            #T1
            temp1 = (h + s1 + ch + K[i] + w[i]) & 0xFFFFFFFF
            #Σ0関数
            s0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            #majority関数
            maj = (a & b) ^ (a & c) ^ (b & c)
            #T2
            temp2 = (s0 + maj) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        # ハッシュの更新
        hash_pieces = [(x + y) & 0xFFFFFFFF for x, y in zip(hash_pieces, [a, b, c, d, e, f, g, h])]

    # 結果の結合
    return ''.join(f'{piece:08x}' for piece in hash_pieces)

'''
# テスト
if __name__ == "__main__":
    test_number = "00009876876536473627364"
    print(f"SHA-256({test_number}) = {tosha256(test_number)}")
'''    