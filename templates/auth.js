function mesajYaz(metin) {
    const alan = document.getElementById("mesaj");
    if (alan) alan.textContent = metin;
}

async function jsonIstegi(adres, veri) {
    const cevap = await fetch(adres, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(veri)
    });
    const sonuc = await cevap.json().catch(() => ({}));
    if (!cevap.ok) throw new Error(sonuc.detail || "İşlem başarısız.");
    return sonuc;
}

const registerForm = document.getElementById("registerForm");
if (registerForm) registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
        const sonuc = await jsonIstegi("/api/auth/kayit", {
            kullanici_adi: document.getElementById("kullanici_adi").value,
            parola: document.getElementById("parola").value
        });
        localStorage.setItem("rotaToken", sonuc.access_token);
        localStorage.setItem("rotaKullaniciAdi", sonuc.kullanici_adi);
        window.location.href = "/uygulama";
    } catch (error) { mesajYaz(error.message); }
});

const loginForm = document.getElementById("loginForm");
if (loginForm) loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
        const sonuc = await jsonIstegi("/api/auth/giris", {
            kullanici_adi: document.getElementById("kullanici_adi").value,
            parola: document.getElementById("parola").value
        });
        localStorage.setItem("rotaToken", sonuc.access_token);
        localStorage.setItem("rotaKullaniciAdi", sonuc.kullanici_adi);
        window.location.href = "/uygulama";
    } catch (error) { mesajYaz(error.message); }
});
