# toplu-tasima-yogunluk-tespiti-uygulamasi
##Ekip Arkadaşları:
  Görkem Hacıoğlu
  Hülya Cerit
  -Diğer arkadaşlarımıza ulaşamadık
## Proje Künyesi

**Takım İsmi:** RotaTech Ekibi

**Takım Rolleri:**
*   **Product Owner:** Görkem Hacıoğlu
*   **Scrum Master:** Hülya Cerit

**Ürün İsmi:** RotaRadar

**Ürün Açıklaması:**
RotaRadar, kitle kaynaklı (crowdsourced) veri toplama modeliyle çalışan, toplu taşıma araçlarındaki (özellikle durağı olmayan dolmuş ve minibüs hatlarındaki) anlık yolcu yoğunluğunu tespit eden bir web uygulamasıdır. Yolcuların araç içinden yaptığı anonim bildirimleri analiz ederek, durakta bekleyen diğer kullanıcılar için gerçek zamanlı bir yoğunluk haritası sunmayı amaçlar.

**Ürün Özellikleri:**
*   **Hızlı Veri Girişi:** Yolcuların hareket halindeki bir araç içinde bile tek tıkla durum (Sakin, Yoğun, Çok Yoğun) bildirebilmesini sağlayan minimalist arayüz.
*   **Gerçek Zamanlı Dinamik Analiz:** Sistemin güncel kalması için yalnızca son 15 dakika içinde girilen verilerin matematiksel ortalamasını alarak nihai bir yoğunluk skoru üretme.
*   **Anti-Spam Koruması:** Asılsız veri akışını ve manipülasyonu engellemek amacıyla, aynı kullanıcının (cihazın) 5 dakika içinde birden fazla bildirim yapmasını engelleyen güvenlik algoritması.
*   **Lokasyon Doğrulaması (Geliştirme Aşamasında):** Kullanıcıların yalnızca fiziksel olarak bulundukları koordinatlarla eşleşen hatlar için bildirim yapabilmesini sağlayan GPS entegrasyonu.

**Hedef Kitle:**
*   Günlük iş veya okul güzergahında dolmuş, minibüs ve otobüs gibi toplu taşıma araçlarını aktif olarak kullanan şehir içi yolcular.
*   Zaman yönetimine önem veren ve dolu bir aracı beklemek yerine alternatif güzergahlar (veya farklı ulaşım yolları) planlamak isteyen bireyler.

## Product Backlog (Ürün İş Listesi)
*   ✅ Kullanıcıların yoğunluk durumunu saniyeler içinde seçebileceği mobil uyumlu web arayüzünün (UI) tasarlanması.
*   ✅ FastAPI kullanılarak backend iskeletinin, Pydantic modellerinin ve API uç noktalarının (endpoints) oluşturulması.
*   ✅ Sistemin tutarlılığı için Zaman Filtresi (Son 15 dk) ve Spam Filtresi (5 dk bekleme) algoritmalarının koda entegre edilmesi.
*   ⏳ HTML5 Geolocation API kullanılarak kullanıcı cihazından anlık enlem/boylam verisinin alınması ve backend'e iletilmesi.
*   ⏳ Toplanan verilerin sonucunun (hattın güncel durumunun) yolculara gösterileceği harita veya durum ekranının tasarlanması.
*   ⏳ Kalıcı veri depolama ve mekansal (spatial) analizler için PostgreSQL/PostGIS veritabanı entegrasyonunun sağlanması.

---


## Sprint 1 Raporu ve Çevik Yönetim (Agile/Scrum)

### Backlog Düzeni ve Story Seçimleri
İlk sprint için odak noktamız MVP'nin (Minimum Viable Product) kalbi olan "Kullanıcı Giriş Katmanı (Data Ingestion)" olarak belirlenmiştir. Bu kapsamda seçilen User Story'ler şunlardır:
*   **Story 1:** Kullanıcıların dolmuş içindeyken yoğunluk durumunu saniyeler içinde seçebileceği mobil uyumlu bir arayüz tasarlanması.
*   **Story 2:** FastAPI ile kullanıcılardan gelen JSON verilerini karşılayacak backend uç noktalarının oluşturulması.
*   **Story 3:** Sistemi manipülasyonlardan korumak için 5 dakikalık "Spam Filtresi" mantığının koda entegre edilmesi.

##2 Daily Scrum (Günlük Toplantılar)
<img width="738" height="1600" alt="image" src="https://github.com/user-attachments/assets/66433ce9-9b15-4564-95ba-4090c3d2564d" />  



##3 Sprint Board (Pano)
Takımımızın iş bölümünü ve görev durumlarını (Idea, To Do, In Progress, Done) takip ettiği sprint panosunun güncel hali:

![Sprint Board Pano Görüntüsü](board.png)
<img width="1902" height="807" alt="board1" src="https://github.com/user-attachments/assets/70c13cd6-2e01-46b0-b39d-ddc4cea8f81e" />
<img width="1859" height="305" alt="board2" src="https://github.com/user-attachments/assets/61bbf108-c541-4c4e-accc-9860f566a5d8" />


### 4. Ürün Durumu (Mevcut Çalışan Sürüm)
İlk sprintin sonunda ortaya çıkan, API ile haberleşen kullanıcı arayüzü ve Swagger test ortamı:

<img width="1456" height="686" alt="Ekran görüntüsü 2026-07-19 190450" src="https://github.com/user-attachments/assets/35c4b227-9c65-46b3-809c-f61859414bb7" />


### 5. Sprint Review (Sprint Değerlendirmesi)
*   **Tamamlananlar:** FastAPI iskeleti kuruldu, Pydantic modelleri hazırlandı. Spam filtresi eklendi ve HTML/JS tabanlı arayüz başarılı bir şekilde sunucuya veri gönderebilir hale getirildi.
*   **Eksikler/Ertelenenler:** Kullanıcının gerçek konumunu (GPS koordinatları) tarayıcıdan HTML5 Geolocation API ile çekme işlemi teknik araştırma gerektirdiği için bir sonraki sprinte aktarıldı.

### 6. Sprint Retrospective (Geçmişe Dönük Analiz)
*   **İyi Gidenler:** Takım içi GitHub Git Flow sürecinin pürüzsüz işlemesi ve backend mantığının (Zaman/Spam filtreleri) planlanandan daha hızlı koda dökülmesi.
*   **Geliştirilmesi Gerekenler:** Projeye başlarken IDE (Cursor/PyCharm) ve terminal entegrasyonlarında yaşanan vakit kayıplarını önlemek için ilerleyen aşamalarda ortam kurulumlarının daha hızlı stabilize edilmesi.
*   




## 🚀 Sprint 2 Raporu

Bu bölüm, takımımızın Sprint 2 boyunca yürüttüğü Çevik (Agile) süreçlerin, toplantı çıktılarının ve ürün ilerleyişinin özetini içermektedir.

### 1. Backlog Düzeni ve Story Seçimleri
Sprint planlama toplantımızda proje hedeflerimize uygun olarak seçtiğimiz kullanıcı hikayeleri (user stories) ve Backlog düzenimiz aşağıda yer almaktadır. İş kalemleri efor ve öncelik sırasına göre değerlendirilerek sprinte dahil edilmiştir.


<img width="1586" height="744" alt="image" src="https://github.com/user-attachments/assets/0b552303-f8a2-47fb-826a-c6733e94f715" />



### 2. Daily Scrum
Sprint boyunca ekip üyeleri olarak senkronizasyonu sağlamak, güncel ilerlemeyi paylaşmak ve olası engelleri (blocker) tespit etmek amacıyla yürüttüğümüz Daily Scrum (Günlük Koordinasyon) akışımızdan bir kesit:

<img width="945" height="502" alt="image" src="https://github.com/user-attachments/assets/55e11f51-3f2f-4933-90d6-ffb681dec65b" />



### 3. Sprint Board (Aktif Sprint Panosu)
Sprint sonu itibarıyla üstlendiğimiz görevlerin güncel durumunu gösteren Kanban/Scrum panomuz. Ekibimizin "To Do", "In Progress" ve "Done" aşamalarındaki şeffaf iş takibi:

<img width="1420" height="845" alt="Ekran görüntüsü 2026-07-19 182652" src="https://github.com/user-attachments/assets/8972b202-a62b-4889-b65f-5b1f52c1d818" />


### 4. Ürün Durumu 
Bu sprint sonunda ürünümüzün geldiği son nokta. Geliştirilen özelliklerin sisteme entegre edilmiş, çalışan güncel hali:

<img width="1918" height="907" alt="Ekran görüntüsü 2026-07-19 185711" src="https://github.com/user-attachments/assets/450c4cec-05b7-4f87-b622-bd40d86dfe37" />



### 5. Sprint Review (Gözden Geçirme)
Sprint sonunda tamamlanan işlerin incelendiği ve ürünün mevcut durumunun değerlendirildiği Sprint Review notlarımız:

Gelecek Planlarımız Sistemin altyapısı şu an daha gelişmiş özellikler eklemeye oldukça müsait.
İlerleyen aşamalarda, kullanıcıların birbirlerinin girdilerini oylayabildiği, fotoğraf yükleyebildiği ve doğal dil işleme ile trafik veya kaza gibi durumların kök neden analizinin yapılabildiği bir sosyal katman entegre etmeyi hedefliyoruz. 
Ayrıca sahte veri girişini tamamen bitirmek için dinamik bir kullanıcı güven skoru algoritması üzerinde çalışıyoruz.


### 6. Sprint Retrospective (Geçmişe Dönük Değerlendirme)
Scrum Master eşliğinde ekibimizin süreçlerini iyileştirmek için yaptığı değerlendirme toplantısı. "Neleri iyi yaptık?", "Neleri geliştirebiliriz?" ve bir sonraki sprint için aldığımız aksiyon kararları:

<img width="1499" height="463" alt="Ekran görüntüsü 2026-07-19 190259" src="https://github.com/user-attachments/assets/9ecbaa9e-800e-4e1e-8e27-869e561b8301" />

