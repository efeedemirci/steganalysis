import wave

def embed_message(audio_path, output_path, message):
    message += '###'  # mesajın sonu
    message_bits = ''.join([format(ord(char), '08b') for char in message])

    # wav dosyasını okur
    audio = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(audio.readframes(audio.getnframes()))

    if len(message_bits) > len(frame_bytes):
        raise ValueError("Mesaj çok uzun, ses dosyasına sığmıyor.")

    for i in range(len(message_bits)):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(message_bits[i])

    modified_audio = wave.open(output_path, 'wb')
    modified_audio.setparams(audio.getparams())
    modified_audio.writeframes(bytes(frame_bytes))
    modified_audio.close()
    audio.close()

    print("✅ Mesaj başarıyla gömüldü.")


def extract_message(audio_path):
    audio = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(audio.readframes(audio.getnframes()))
    bits = [str(byte & 1) for byte in frame_bytes]

    message = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        char = chr(int(''.join(byte), 2))
        message += char
        if message.endswith('###'):
            break

    audio.close()
    return message.rstrip('###')


if __name__ == "__main__":
    print("LSB Ses Steganografi")
    print("1. Mesaj Gizle")
    print("2. Mesaj Çıkar")
    secim = input("Seçiminizi yapın (1/2): ")

    if secim == '1':
        input_audio = "input.wav"
        output_audio = "output.wav"
        msg = input("Gizlenecek mesaj (160 karaktere kadar): ")[:160]
        embed_message(input_audio, output_audio, msg)
    elif secim == '2':
        stego_audio = "output.wav"
        gizli_mesaj = extract_message(stego_audio)
        print(f"Gizli Mesaj: {gizli_mesaj}")
    else:
        print("Geçersiz seçim.")