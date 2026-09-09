# PRESENTASI TUGAS 1
## Analisis dan Desain Sistem – IF21307
### Program Studi Informatika, Universitas Jenderal Soedirman

---

## SLIDE 1 – COVER

**SISTEM INFORMASI LAYANAN PEMESANAN KONTEN**
**MEDKREMINFO BEM FAKULTAS TEKNIK UNSOED**

Tugas 1 – Penyusunan Project Charter dan Analisis Awal Proyek Sistem Informasi

| Nama | NIM | Peran |
|---|---|---|
| Timotius Willy Narendra | H1D025052 | Project Manager |
| Fardizza Vinda Rahman | H1D025067 | Sistem Analis |
| Adridinan Najmi Faza | H1D025059 | Programmer |
| Salman Thufail | H1D022109 | Programmer |

Purbalingga, September 2026

---

## SLIDE 2 – LATAR BELAKANG MASALAH

**Siapa itu Medkreminfo?**
Kementerian Media, Kreatif, dan Informasi BEM FT UNSOED — pengelola konten di 4 kanal resmi:
- 📸 Instagram Feeds
- 📱 Instagram Story
- 💼 LinkedIn
- 🎵 TikTok

**Masalah yang ada sekarang:**
> *"Semua pemesanan konten dilakukan lewat WhatsApp personal ke PJ masing-masing kementerian"*

❌ Brief konten tenggelam di riwayat chat
❌ Menteri kesulitan memantau keseluruhan beban kerja
❌ Deadline sering miskomunikasi
❌ Format konten sering salah (rasio, spesifikasi kanal)
❌ Beban kerja staf tidak merata

---

## SLIDE 3 – HASIL WAWANCARA (BUKTI LAPANGAN)

**Narasumber:** Aba Ibrahim – Staf Medkreminfo BEM FT

> *"Normalnya seminggu bisa 5–10 request. Kalau lagi ada acara besar bisa tembus 15–20. Semua masuk lewat chat dan susah dilacak."*

> *"Pernah coba Trello, tapi nggak jalan. Akhirnya balik ke WhatsApp lagi."*

> *"Yang paling sering itu pesanan tenggelam di chat, terus lupa dikerjain. Deadline juga sering salah paham."*

**Temuan Kunci:**
| Aspek | Kondisi As-Is |
|---|---|
| Media koordinasi | WhatsApp (100%) |
| Sistem sebelumnya | Trello – gagal, tidak konsisten |
| Volume request | 5–10/minggu, puncak 15–20 |
| Kanal terbanyak | Instagram Feeds |
| Akar masalah | Desentralisasi, tidak ada tracking |

---

## SLIDE 4 – TUJUAN PROYEK

Membangun **Sistem Informasi Layanan Pemesanan Konten** berbasis *web* (*ticketing system*) untuk:

1. ✅ **Standarisasi** alur pemesanan dari 14 kementerian BEM FT
2. ✅ **Spesifikasi kanal** terstruktur sejak formulir (feeds, story, LinkedIn, TikTok)
3. ✅ **Transparansi** — kementerian pemesan bisa pantau status real-time
4. ✅ **Distribusi kerja merata** — Admin bisa assign tugas sesuai keahlian staf
5. ✅ **Eliminasi miskomunikasi** — semua brief & aset tersimpan terpusat

---

## SLIDE 5 – SOLUSI YANG DIUSULKAN

**Sistem dengan 3 Level Akses:**

| Peran | Hak Akses |
|---|---|
| 👑 Admin (Menteri) | Lihat semua pesanan, assign tugas, kelola akun, pantau kalender |
| 🛠️ Eksekutor (Staf) | Lihat tugas sesuai keahlian, unduh lampiran, update status |
| 📋 Klien (Kementerian) | Buat request, isi formulir terstruktur, pantau status pesanan sendiri |

**Alur Tiket:**
`Draft → Submitted → In Progress → Review/Revision → Ready to Post → Published`

---

## SLIDE 6 – FITUR UTAMA SISTEM

1. **📝 Formulir Pemesanan Multi-Kanal**
   - Form adaptif sesuai kanal (rasio, naskah, aset)
   - Admin bisa validasi, revisi, atau setujui

2. **👥 Manajemen Penugasan & Spesialisasi Staf**
   - Assign ke staf berdasarkan keahlian (desainer grafis / video editor / copywriter)
   - Re-assign jika staf overload

3. **📅 Kalender Editorial Publikasi**
   - Visualisasi jadwal tayang semua kanal
   - Cegah bentrok jadwal publikasi

4. **🔔 Pelacakan Status & Notifikasi**
   - Update real-time status tiket
   - Notifikasi saat ada tugas baru atau revisi

5. **🔐 Autentikasi Berbasis Peran (RBAC)**
   - 3 tingkatan: Admin, Eksekutor, Klien

---

## SLIDE 7 – BATASAN PROYEK (OUT OF SCOPE)

Apa yang **TIDAK** dikerjakan sistem ini:

| ❌ Tidak Termasuk | Alasan |
|---|---|
| Auto-posting ke medsos (API Instagram/TikTok) | Di luar kapasitas dan lingkup semester |
| Editor grafis/video di dalam web | Software eksternal tetap dipakai (Canva, Premiere, dll.) |
| Kelola komentar & DM medsos | Bukan manajemen konten |
| Pesanan dari pihak eksternal/sponsor | Hanya internal BEM FT |

---

## SLIDE 8 – STAKEHOLDER

| Stakeholder | Peran | Kepentingan |
|---|---|---|
| Menteri Medkreminfo | Admin Sistem | Kontrol penuh manajemen konten & SDM |
| Staf Medkreminfo | Eksekutor | Terima tugas sesuai keahlian, update progress |
| 14 Kementerian BEM FT | Klien | Ajukan request, pantau status |
| Ketua BEM FT | Sponsor | Wewenang mewajibkan pemakaian sistem |
| Tim Pengembang (Kami) | Developer | Membangun & menyerahkan sistem |

---

## SLIDE 9 – ESTIMASI ANGGARAN & JADWAL

**Anggaran (Hipotesis):**

| Komponen | Biaya |
|---|---|
| Manajer Proyek | Rp 2.000.000 |
| Sistem Analis | Rp 1.500.000 |
| Programmer × 2 | Rp 2.500.000 |
| Sewa Hosting & Domain | Rp 750.000 |
| **TOTAL** | **Rp 6.750.000** |

**Jadwal (50 Hari):**

| Fase | Durasi |
|---|---|
| 1. Persiapan Project | 3 Hari |
| 2. Perencanaan | 3 Hari |
| 3. Pelaksanaan (Coding & Desain) | 30 Hari |
| 4. Testing & Maintenance | 10 Hari |
| 5. Penutup & Serah Terima | 4 Hari |

---

## SLIDE 10 – RISIKO PROYEK

| # | Risiko | Dampak | Mitigasi |
|---|---|---|---|
| 1 | User resistance – pengguna enggan beralih dari WhatsApp | Tinggi | UI simpel + instruksi tegas dari Ketua BEM |
| 2 | Scope creep – permintaan fitur terus bertambah | Sedang | Kunci kesepakatan fitur di awal proyek |
| 3 | Proyek melewati batas waktu semester | Tinggi | Jadwal ketat + milestone mingguan |
| 4 | Server/Hosting down saat beban tinggi | Rendah | Pilih provider hosting terpercaya |

---

## SLIDE 11 – TIM & PEMBAGIAN PERAN

| Nama | NIM | Peran | Kontribusi Utama |
|---|---|---|---|
| Timotius Willy Narendra | H1D025052 | Project Manager | Koordinasi tim, penyusunan project charter, wawancara narasumber |
| Fardizza Vinda Rahman | H1D025067 | Sistem Analis | Analisis kebutuhan, stakeholder map, scope statement |
| Adridinan Najmi Faza | H1D025059 | Programmer | Arsitektur sistem, rencana database & teknologi |
| Salman Thufail | H1D022109 | Programmer | Risk register, estimasi anggaran & jadwal |

---

## SLIDE 12 – PENUTUP

**Kesimpulan:**

> Medkreminfo BEM FT membutuhkan sistem terpusat berbasis web untuk menggantikan alur WhatsApp yang tidak terstruktur. Sistem Informasi Layanan Pemesanan Konten ini akan meningkatkan efisiensi, transparansi, dan akuntabilitas pengelolaan konten BEM FT.

**Deliverables yang akan dihasilkan:**
1. Aplikasi Web Sistem Informasi (siap pakai)
2. Dokumen SRS & SDD + Source Code
3. User Manual (Admin, Staf, Kementerian Pemesan)
4. Berita Acara Serah Terima ke BEM FT

---

*Terima Kasih*
**Kelompok XX – Analisis dan Desain Sistem – IF21307**
*Universitas Jenderal Soedirman, 2026*
