# 🔐 Steganalysis Techniques Project

Bu proje, ses ve video dosyalarında 160 karaktere kadar mesaj saklamak ve bu mesajı geri çıkartmak için çeşitli **steganaliz algoritmalarını** kullanır.

## 📁 Kapsanan Teknikler

1. **LSB (Least Significant Bit) Algoritması**  
   - Görüntünün en düşük bitlerine veri gömülür.
   - Hem ses hem de görüntü dosyalarında uygulanabilir.

2. **JPEG (DCT - Discrete Cosine Transform) Algoritması**  
   - JPEG görüntülerde frekans dönüşüm katsayılarına veri gömülür.

3. **BPCS (Bit Plane Complexity Segmentation) Algoritması**  
   - Görüntünün karmaşık bit düzlemlerine veri yerleştirilir.
   - Genellikle PNG türü kayıpsız görüntülerle çalışır.

4. **Maskeleme ve Filtreleme Yöntemleri**  
   - Görüntü üzerindeki bölgelere maskeleme uygulanarak veri gizlenir.
   - Görselin insan algısına uygun bölgeleri hedefler.

5. **Sezgisel (Heuristic) Steganaliz Yöntemleri**  
   - WAV dosyalarının örneklerinde bit düzeyinde analiz yapılarak veri saklanır.
   - İstatistiksel olarak düşük fark oluşturan alanlar seçilir.
