// auth.js

// 1. KAYIT İŞLEMİ (Register)
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const isim = document.getElementById('isim').value;
        const soyisim = document.getElementById('soyisim').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (password.length < 6) {
            alert("Şifreniz en az 6 karakter olmalıdır!");
            return;
        }

        const response = await fetch('http://127.0.0.1:8000/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ isim, soyisim, email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz.");
            window.location.href = "/";
        } else {
            alert("Hata: " + data.detail);
        }
    });
}

// 2. GİRİŞ İŞLEMİ (Login)
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Hoşgeldin, " + data.isim + "!");
            window.location.href = "/uygulama";
        } else {
            alert("Hata: " + data.detail);
        }
    });
}

// 3. ŞİFRE YENİLEME İŞLEMİ (Reset Password)
const resetForm = document.getElementById('resetForm');
if (resetForm) {
    resetForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const new_password = document.getElementById('new_password').value;

        if (new_password.length < 6) {
            alert("Yeni şifreniz en az 6 karakter olmalıdır!");
            return;
        }

        const response = await fetch('http://127.0.0.1:8000/api/auth/reset-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, new_password })
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            window.location.href = "/";
        } else {
            alert("Hata: " + data.detail);
        }
    });
}