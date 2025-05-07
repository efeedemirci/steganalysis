import cv2
import numpy as np

def embed_message_mask(image_path, message, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3) + cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    edges = np.uint8(np.absolute(edges))
    _, mask = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)

    # Mesajı bitlere çevirelim
    message += "###"
    bits = ''.join([format(ord(c), '08b') for c in message])

    bit_idx = 0
    stego = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[i, j] == 255 and bit_idx < len(bits):  # sadece kenar piksellerine yaz
                stego[i, j] = (stego[i, j] & 0xFE) | int(bits[bit_idx])
                bit_idx += 1

    cv2.imwrite(output_path, stego)
    print("Mesaj başarıyla gömüldü.")

def extract_message_mask(stego_path):
    img = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3) + cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    edges = np.uint8(np.absolute(edges))
    _, mask = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)

    bits = ''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[i, j] == 255:
                bits += str(img[i, j] & 1)

    message = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        message += char
        if message.endswith('###'):
            break

    return message.rstrip('###')

if __name__ == "__main__":
    print("Maskeleme ve Filtreleme Steganografi")
    print("1. Mesaj Gömmek")
    print("2. Mesaj Çıkarmak")
    choice = input("Seçiminizi yapın (1/2): ")

    if choice == "1":
        img_path = "lena.png"
        msg = input("Gizlenecek mesaj (160 karaktere kadar): ")
        output = "donna.png"
        embed_message_mask(img_path, msg[:160], output)

    elif choice == "2":
        stego_path = "donna.png"
        message = extract_message_mask(stego_path)
        print("Çıkarılan Mesaj:", message)

    else:
        print("Geçersiz seçim.")
