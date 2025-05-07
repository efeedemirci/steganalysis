import wave
import numpy as np

def embed_message_wav(input_wav, message, output_wav):
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        samples = np.frombuffer(frames, dtype=np.int16).copy()

    message += '###'
    bits = ''.join(format(ord(c), '08b') for c in message)

    # Sezgisel olarak sadece yüksek genlikli örneklere gömme
    indices = np.where(np.abs(samples) > 500)[0]  # eşik değeri

    if len(indices) < len(bits):
        print("Yeterli yer yok")
        return

    for i, bit in enumerate(bits):
        val = int(samples[indices[i]])  # int16 değeri alınır
        unsigned_val = val + 65536 if val < 0 else val  # signed to unsigned
        new_val = (unsigned_val & 0xFFFE) | int(bit)
        new_val = new_val % 65536  # güvenli sınır içinde kal
        samples[indices[i]] = np.int16(new_val if new_val <= 32767 else new_val - 65536)


    with wave.open(output_wav, 'wb') as outwav:
        outwav.setparams(params)
        outwav.writeframes(samples.astype(np.int16).tobytes())

    print("Mesaj WAV dosyasına gömüldü:", output_wav)

def extract_message_wav(stego_wav):
    with wave.open(stego_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        samples = np.frombuffer(frames, dtype=np.int16)

    indices = np.where(np.abs(samples) > 500)[0]

    bits = ''
    for i in indices:
        bits += str(samples[i] & 1)

    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    message = ''.join(chars)
    return message.split('###')[0]

# Örnek kullanım
if __name__ == "__main__":
    print("WAV Steganografi")
    print("1. Mesaj Gömmek")
    print("2. Mesaj Çıkarmak")
    secim = input("Seçiminiz (1/2): ")

    if secim == '1':
        in_wav = "input.wav"
        out_wav = "output.wav"
        msg = input("Gizlenecek mesaj (160 karakter max): ")
        embed_message_wav(in_wav, msg[:160], out_wav)
    elif secim == '2':
        in_wav = "output.wav"
        print("Mesaj:", extract_message_wav(in_wav))
    else:
        print("Geçersiz seçim")
