import numpy as np
import cv2
from scipy.fft import dst, idst

def embed_message(image_path, output_path, message):
    message += '###' 
    message_bits = ''.join(format(ord(char), '08b') for char in message)
    bit_index = 0

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    img = img[:h - h % 8, :w - w % 8]  # 8x8 bloklara bölünebilir hale getir

    blocks = [img[i:i+8, j:j+8] for i in range(0, h, 8) for j in range(0, w, 8)]
    dst_blocks = []

    for block in blocks:
        b = dst(dst(block.T, type=2).T, type=2)
        if bit_index < len(message_bits):
            coeff = int(b[4, 4])
            coeff = (coeff & ~1) | int(message_bits[bit_index])
            b[4, 4] = coeff
            bit_index += 1
        dst_blocks.append(b)

    stego_blocks = [idst(idst(b.T, type=2).T, type=2) / 4 for b in dst_blocks]

    out_img = np.zeros_like(img)
    index = 0
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            out_img[i:i+8, j:j+8] = np.clip(stego_blocks[index], 0, 255)
            index += 1

    cv2.imwrite(output_path, np.uint8(out_img))
    print("Mesaj başarıyla DCT kullanılarak gömüldü.")


def extract_message(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    img = img[:h - h % 8, :w - w % 8]

    blocks = [img[i:i+8, j:j+8] for i in range(0, h, 8) for j in range(0, w, 8)]

    bits = ''
    for block in blocks:
        b = dst(dst(block.T, type=2).T, type=2)
        coeff = int(b[4, 4])
        bits += str(coeff & 1)

    message = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(''.join(byte), 2))
        message += char
        if message.endswith('###'):
            break

    return message.rstrip('###')


if __name__ == "__main__":
    print("DST Görsel Steganografi")
    print("1. Mesaj Gizle")
    print("2. Mesaj Çıkar")
    secim = input("Seçiminiz (1/2): ")

    if secim == '1':
        img_path = "lena.jpeg"
        output_path = "lena_is_a_spy.jpeg"
        mesaj = input("Gizlenecek mesaj (160 karaktere kadar): ")[:160]
        embed_message(img_path, output_path, mesaj)
    elif secim == '2':
        img_path = "lena_is_a_spy.jpeg"
        msg = extract_message(img_path)
        print(f"Çıkarılan Mesaj: {msg}")
    else:
        print("Geçersiz seçim.")
