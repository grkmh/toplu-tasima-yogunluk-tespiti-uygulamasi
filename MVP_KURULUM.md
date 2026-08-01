# RotaRadar MVP'yi çalıştırma

Bu sürüm `guncel` branch'i temel alınarak hazırlanmıştır. Varsayılan veritabanı
`rotaradar_mvp.db` dosyasıdır; mevcut `rotaradar.db` dosyanızı silmez veya değiştirmez.

## Kurulum

VS Code terminalinde, proje klasöründeyken:

```powershell
venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Ardından `http://127.0.0.1:8001` adresini açın. Önce kullanıcı oluşturun, sonra
uygulamada yolculuk kaydı ve fotoğraf paylaşımını deneyin.

Tamamlanan yolculukların biniş ve iniş yoğunluğu ortalaması alınır. Uygulamanın
üstündeki grafik, bu puanların hat bazında tüm zamanlar ortalamasını ve kaç
yolculuktan hesaplandığını gösterir. Yeni bir yolculuk bitince grafik yenilenir.

## Veriler nerede?

- Kullanıcılar, yolculuklar ve paylaşım bilgileri: `rotaradar_mvp.db`
- Yüklenen ve güvenli biçimde yeniden kaydedilen fotoğraflar: `uploads/`

Bu iki konum `.gitignore` içindedir; kişisel veri ve fotoğraflar GitHub'a gönderilmez.

## GitHub'a göndermeden önce

```powershell
git status
git add .
git commit -m "Kullanici girisi ve fotograf paylasimi eklendi"
git push origin guncel
```

`git status` çıktısında `rotaradar_mvp.db` ve `uploads/` görünmemelidir.

## Önemli MVP sınırı

Bu yerel prototipte SQLite ve fotoğraf klasörü uygulamanın çalıştığı bilgisayardadır.
İnternete açılacak sürümde kalıcı disk sunan bir barındırma hizmeti veya ayrı bir
dosya depolama servisi gerekir. Bu dağıtım işi prototip doğrulandıktan sonra yapılmalıdır.
