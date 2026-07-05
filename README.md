# toplu-tasima-yogunluk-tespiti-uygulamasi
## 🏃‍♂️ Sprint 1 Raporu ve Çevik Yönetim (Agile/Scrum)

Bu bölümde, takımımızın ilk sprint (koşu) döngüsündeki yönetim süreçleri ve ürün çıktıları belgelenmiştir. 

### 1. Backlog Düzeni ve Story Seçimleri
İlk sprint için odak noktamız MVP'nin (Minimum Viable Product) kalbi olan "Kullanıcı Giriş Katmanı (Data Ingestion)" olarak belirlenmiştir. Bu kapsamda seçilen User Story'ler şunlardır:
*   **Story 1:** Kullanıcıların dolmuş içindeyken yoğunluk durumunu saniyeler içinde seçebileceği mobil uyumlu bir arayüz tasarlanması.
*   **Story 2:** FastAPI ile kullanıcılardan gelen JSON verilerini karşılayacak backend uç noktalarının oluşturulması.
*   **Story 3:** Sistemi manipülasyonlardan korumak için 5 dakikalık "Spam Filtresi" mantığının koda entegre edilmesi.

### 2. Daily Scrum (Günlük Toplantılar)
*   **İletişim:** Günlük planlamalar ve kod çakışmalarının önlenmesi takım içi iletişim kanalları (Discord/WhatsApp) üzerinden sağlanmıştır.
*   **Çözülen Engeller:** Frontend ve Backend'in farklı portlarda çalışmasından kaynaklı CORS (Cross-Origin Resource Sharing) hataları gün içindeki değerlendirmelerle çözülmüş ve uçtan uca veri akışı sağlanmıştır.

### 3. Sprint Board (Pano)
Takımımızın iş bölümünü ve görev durumlarını (To Do, In Progress, Done) takip ettiği sprint panosunun güncel hali:

> **Not:** *(Trello, Jira, GitHub Projects veya Notion üzerinde kullandığınız görev panosunun ekran görüntüsünü alıp projeye `board.png` olarak kaydedin ve buraya ekleyin)*
![Sprint Board Pano Görüntüsü](board.png)

### 4. Ürün Durumu (Mevcut Çalışan Sürüm)
İlk sprintin sonunda ortaya çıkan, API ile haberleşen kullanıcı arayüzü ve Swagger test ortamı:

> **Not:** *(Hazırladığımız index.html dosyasının tarayıcıdaki görüntüsünü ve Swagger API ekranını yan yana koyup ekran görüntüsü alarak `urun.png` adıyla buraya ekleyin)*
![Uygulama Arayüzü ve Backend](image/urun.png)

### 5. Sprint Review (Sprint Değerlendirmesi)
*   **Tamamlananlar:** FastAPI iskeleti kuruldu, Pydantic modelleri hazırlandı. Spam filtresi sisteme entegre edildi ve HTML/JS tabanlı arayüz başarılı bir şekilde sunucuya veri gönderebilir hale getirildi.
*   **Eksikler/Ertelenenler:** Kullanıcının gerçek konumunu (GPS koordinatları) tarayıcıdan HTML5 Geolocation API ile çekme işlemi teknik araştırma gerektirdiği için bir sonraki sprinte aktarıldı.

### 6. Sprint Retrospective (Geçmişe Dönük Analiz)
*   **İyi Gidenler:** Takım içi GitHub Git Flow sürecinin pürüzsüz işlemesi ve backend mantığının (Zaman/Spam filtreleri) planlanandan daha hızlı koda dökülmesi.
*   **Geliştirilmesi Gerekenler:** Projeye başlarken IDE (Cursor/PyCharm) ve terminal entegrasyonlarında yaşanan vakit kayıplarını önlemek için ilerleyen aşamalarda ortam kurulumlarının daha hızlı stabilize edilmesi.