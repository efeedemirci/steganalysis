import numpy as np
import cv2
import math

def calculate_complexity(bit_plane):
    """Hesaplama için karmaşıklık ölçümü yapma (entropi)"""
    unique, counts = np.unique(bit_plane, return_counts=True)
    probs = counts / bit_plane.size
    entropy = -np.sum(probs * np.log2(probs + 1e-10))  # Küçük epsilon ekleyerek log(0)'dan kaçınıyoruz
    return entropy

def embed_message(image_path, output_path, message):
    message += '###'  # Mesaj sonu belirteci
    message_bits = ''.join(format(ord(ch), '08b') for ch in message)
    bit_index = 0

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    # Görüntü bit düzeylerini ayırma
    bit_planes = []
    for i in range(8):
        bit_planes.append(((img >> i) & 1))

    # Karmaşıklık analizini yapma
    complexities = [calculate_complexity(plane) for plane in bit_planes]

    # Mesajı en karmaşık bit düzeyine yerleştirme
    for i in range(8):  # En karmaşık düzey en yüksek entropiye sahip olmalı
        if complexities[i] == max(complexities):
            target_plane = i
            break

    # Mesaj bitlerini hedef düzeyin LSB'sine yerleştirme
    for i in range(h):
        for j in range(w):
            if bit_index < len(message_bits):
                bit = int(message_bits[bit_index])
                img[i, j] = (img[i, j] & (255 ^ (1 << target_plane))) | (bit << target_plane)
                bit_index += 1

    cv2.imwrite(output_path, img)
    print("BPCS ile mesaj başarıyla gömüldü.")

def extract_message(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    # Görüntü bit düzeylerini ayırma
    bit_planes = []
    for i in range(8):
        bit_planes.append(((img >> i) & 1))

    # Karmaşıklık analizini yapma
    complexities = [calculate_complexity(plane) for plane in bit_planes]

    # Mesajı en karmaşık bit düzeyinden çıkarma
    for i in range(8):
        if complexities[i] == max(complexities):
            target_plane = i
            break

    message_bits = ''
    for i in range(h):
        for j in range(w):
            bit = (img[i, j] >> target_plane) & 1
            message_bits += str(bit)

    message = ''
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        message += char
        if message.endswith('###'):
            break

    return message.rstrip('###')

if __name__ == "__main__":
    print("BPCS Steganografi")
    print("1. Mesaj Gömmek")
    print("2. Mesaj Çıkarmak")
    secim = input("Seçiminizi yapın (1/2): ")

    if secim == '1':
        img_path = "lena.png"
        output_path = "lenna.png"
        msg = input("Gizlenecek mesaj (160 karaktere kadar): ")[:160]
        embed_message(img_path, output_path, msg)
    elif secim == '2':
        img_path = "lenna.png"
        message = extract_message(img_path)
        print(f"Çıkarılan Mesaj: {message}")
    else:
        print("Geçersiz seçim.")