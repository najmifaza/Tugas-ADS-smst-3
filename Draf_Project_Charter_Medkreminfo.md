# SISTEM INFORMASI LAYANAN PEMESANAN KONTEN MEDKREMINFO
## STUDI KASUS BEM FAKULTAS TEKNIK
## PROJECT CHARTER

Version <1.0>
<15 September 2024>

Disusun oleh:

**Project Manager**
[Nama Anda] ([NIM Anda])

**Anggota**
Timotius Willy Narendra (H1D025052)
Fardizza Vinda Rahman (H1D025067)
Adridinan Najmi Faza (H1D025059)
Salman Thufail (H1D022109)

---

## Business Case

### 1.0 Latar Belakang

Penggunaan teknologi informasi di dalam organisasi kemahasiswaan sangat krusial untuk menjaga kelancaran alur kerja. Pada Badan Eksekutif Mahasiswa Fakultas Teknik (BEM FT), kementerian Media, Kreatif, dan Informasi (Medkreminfo) bertanggung jawab atas seluruh produksi konten visual, audio-visual, serta pengelolaan media sosial resmi organisasi. Terdapat empat (4) kanal publikasi utama yang dikelola, yaitu:
1. **Instagram Feeds** (desain mikroblog, poster acara, carousel edukatif, dan pengumuman resmi).
2. **Instagram Story** (publikasi cepat, live report, broadcast informasi penting, serta interaksi kuis/polling).
3. **LinkedIn** (publikasi profesional, rekap pencapaian prestasi, relasi kemitraan, dan siaran pers kegiatan).
4. **TikTok** (video pendek vertikal interaktif, tren kreatif mahasiswa, edukasi, dan dokumentasi santai).

Saat ini, terdapat permasalahan pada alur pemesanan konten dari 14 kementerian lain ke Medkreminfo. Sistem yang berjalan saat ini bersifat desentralisasi, di mana Medkreminfo membagi stafnya menjadi Penanggung Jawab (PJ) untuk masing-masing kementerian. Kementerian pemesan akan melakukan *request* (permintaan) desain secara manual melalui *personal chat* WhatsApp langsung kepada PJ masing-masing. Hal ini menyebabkan Menteri Medkreminfo kesulitan melacak keseluruhan beban kerja, hilangnya detail *brief* konten di riwayat *chat*, ketidakjelasan batas waktu pengerjaan (*deadline*), ketidaksesuaian spesifikasi format antar kanal media sosial, dan PJ sering kali kewalahan jika kementerian yang dipegangnya sedang memiliki banyak *request* bersamaan. 

Berdasarkan permasalahan tersebut, kami bertujuan untuk membantu Medkreminfo BEM FT dalam mengelola data pesanan konten secara terpusat agar proses kerja lebih efektif dan efisien. Kami mengusulkan pembuatan Sistem Informasi Layanan Pemesanan Konten berbasis *web* (*ticketing system*) untuk memecahkan permasalahan desentralisasi dan manajemen penugasan tersebut.

### 2.0 Tujuan Bisnis

Tujuan dari pembuatan sistem informasi ini meliputi beberapa aspek utama:
1. **Standarisasi Alur Pemesanan**: Menyeragamkan format dan prosedur pengajuan *request* konten dari seluruh kementerian di BEM FT agar data serta *brief* tersimpan secara terpusat dan tidak tercecer.
2. **Spesifikasi Kanal yang Terstruktur**: Mengakomodasi spesifikasi teknis khusus untuk setiap kanal publikasi (Instagram Feeds, Instagram Story, LinkedIn, TikTok) sejak awal pengisian formulir, sehingga meminimalisir revisi akibat salah ukuran atau ketidaklengkapan aset.
3. **Mempermudah Staf yang Bertugas**: Memberikan kemudahan bagi staf eksekutor Medkreminfo dalam menerima detail *brief*, mengakses materi pendukung, serta memperbarui status progres pengerjaan secara langsung dan terstruktur tanpa bergantung pada riwayat *chat* personal.
4. **Optimalisasi Manajemen SDM Medkreminfo**: Mempermudah kementerian Medkreminfo dalam mengelola sumber daya manusia (SDM), membagi beban kerja penugasan secara adil dan merata (*workload balancing*) sesuai keahlian staf (misal: desainer grafis vs editor video), serta memantau kapasitas staf secara transparan.
5. **Transparansi bagi Kementerian Pemesan**: Mempermudah kementerian pemesan dalam memantau tahapan pengerjaan konten secara *real-time* tanpa harus terus-menerus menanyakan konfirmasi secara manual melalui *chat*.

### 3.0 Asumsi dan Kendala

Pembuatan sistem informasi ini bertujuan untuk menyelesaikan kendala yang dialami Medkreminfo BEM FT, di antaranya yaitu:
*   Ketidakteraturan format *brief* pemesanan konten karena dikirim via *chat* WhatsApp langsung ke PJ kementerian.
*   Menteri Medkreminfo kesulitan memonitor *progress* pengerjaan karena komunikasi terjadi secara privat (desentralisasi).
*   Beban kerja staf (PJ) Medkreminfo sangat bergantung pada seberapa aktif kementerian yang dipegangnya, sehingga distribusi kerja tidak merata.
*   Sering terjadi ketidakjelasan atau kesalahan format konten antara kebutuhan Instagram Feeds (1:1 / 4:5), Instagram Story (9:16), LinkedIn (rilis formal & infografis), maupun TikTok (video vertikal 9:16).
*   Sering terjadinya miskomunikasi terkait *deadline* publikasi jika PJ sedang berhalangan.

### 4.0 Keperluan Awal Proyek

Proyek ini dapat berjalan jika mendapatkan dukungan dari pihak BEM FT yang meliputi:
1. Dukungan dari Ketua BEM FT dan Menteri Medkreminfo untuk mewajibkan penggunaan sistem ini.
2. Mempelajari dan mengerti alur kerja serta kebutuhan staf Medkreminfo.
3. Mempelajari dan mengerti kesulitan kementerian lain saat memesan konten.
4. Mempersiapkan Team Project dan infrastruktur *hosting/server*.

### 5.0 Estimasi Anggaran

Untuk membangun Sistem Informasi Pemesanan Konten, dianggarkan biaya hipotesis dengan rincian sebagai berikut:

| No | Keterangan | Waktu | Biaya |
|---|---|---|---|
| 1 | Sistem Informasi | 45 hari | Rp 6.000.000,00 |
| | Manajer Proyek | | Rp 2.000.000,00 |
| | Sistem Analis | | Rp 1.500.000,00 |
| | Programmer (Rp 1.250.000) x 2 | | Rp 2.500.000,00 |
| 2 | Infrastruktur | 3 hari | Rp 750.000,00 |
| | Sewa Hosting & Domain (1 Tahun) | | Rp 750.000,00 |
| | **TOTAL BIAYA** | | **Rp 6.750.000,00** |

### 6.0 Estimasi Jadwal

Proyek pengembangan Sistem Informasi Pemesanan Konten direncanakan selama 50 Hari. Berikut estimasi jadwal secara garis besar:
1. Persiapan Project : 3 Hari
2. Perencanaan : 3 Hari
3. Pelaksanaan (Coding & Desain) : 30 Hari
4. Testing & Maintenance : 10 Hari
5. Penutup & Serah Terima : 4 Hari

### 7.0 Resiko potential

Terdapat beberapa risiko pada proyek ini. Risiko terbesar adalah *user resistance* (pengguna enggan memakai sistem karena sudah terbiasa dengan WhatsApp). Untuk mengatasi masalah tersebut, sistem harus dirancang dengan *User Interface* (UI) yang sangat sederhana dan membutuhkan instruksi tegas dari pimpinan BEM. Risiko lain adalah *scope creep* (permintaan penambahan fitur terus-menerus). Berikut urutan risiko prioritas:
1. Pengurus BEM enggan bertransisi menggunakan sistem baru.
2. Pendefinisian fitur yang kurang merinci di awal.
3. Penyelesaian proyek melewati batas waktu semester perkuliahan.
4. Server/Hosting mengalami *down* saat beban tinggi.

---

## PROJECT CHARTER

### SISTEM INFORMASI LAYANAN PEMESANAN KONTEN MEDKREMINFO

**Project Title** : Sistem Informasi Pemesanan Konten Medkreminfo
**Project Start Date** : 15 September 2024
**Project Finished Date** : 4 November 2024

**Budget Information** :
Proyek ini diestimasikan membutuhkan dana pengembangan dan infrastruktur sebesar Rp 6.750.000,00 (hipotesis). Pengerjaan dilakukan oleh tim pengembang mahasiswa dengan estimasi pengerjaan selama 50 hari kalender kerja.

**Project Objective** :
Sistem Informasi Pemesanan Konten merupakan sebuah sistem internal (*ticketing system*) yang dirancang khusus untuk memfasilitasi, menstandarisasi, dan mencatat seluruh alur birokrasi *request* publikasi media di lingkungan BEM FT. Sistem ini memusatkan pengajuan konten untuk 4 kanal publikasi resmi:
1. **Instagram Feeds**: Desain poster, infografis, carousel, dan mikroblog edukatif.
2. **Instagram Story**: Publikasi cepat, live report, broadcast info penting, dan interaksi audiens.
3. **LinkedIn**: Rilis pers formal, rekap pencapaian prestasi, relasi kemitraan, dan profil kegiatan organisasi.
4. **TikTok**: Video pendek kreatif vertikal (format 9:16), edukasi ringan, recap kegiatan, dan konten tren.

Dengan sistem ini, detail *brief* serta aset untuk tiap kanal tidak lagi tercecer di *chat* personal, dan distribusi tugas antar staf Medkreminfo menjadi terukur.

Dalam sistem ini terdapat tiga (3) pihak yang memiliki hak akses berbeda, di antaranya:
a) **Admin (Menteri Medkreminfo)** : Memiliki hak akses penuh untuk melihat semua pesanan masuk, membagikan (*assign*) tugas ke staf tertentu, memantau kalender publikasi, dan mengelola akun pengguna.
b) **Eksekutor (Staf Medkreminfo)** : Memiliki hak akses untuk melihat tugas yang diberikan kepadanya sesuai bidang keahlian (desain grafis / video editor / copywriter), mengunduh lampiran, dan mengubah status progres pengerjaan (misal: *In Progress*, *Review*, *Done*).
c) **Klien (Kementerian Lain)** : Memiliki hak akses untuk membuat *request* konten baru dengan menentukan kanal tujuan melalui formulir terstruktur, serta memantau status progres pesanan mereka sendiri secara transparan.

**Pendekatan** :
1. Melakukan wawancara langsung dengan perwakilan Medkreminfo (Sdr. Baim) untuk mendapatkan informasi alur kerja yang valid.
2. Menentukan arsitektur *web*, *Database Engine* (MySQL), dan Bahasa Pemrograman yang akan dipakai.
3. Menjadwalkan kegiatan pengerjaan proyek sesuai tenggat waktu mata kuliah.

**Project Manager** :
**Timotius Willy Narendra**

#### Roles and Responsibilities

| Name | Role | Position | Contact Information |
|---|---|---|---|
| Aba Ibrahim  | Sponsor / Narasumber | Staf Medkreminfo BEM FT | aba.ibrahim@mhs.unsoed.ac.id |
| Timotius Willy Narendra | Team Member | Project Manager | timotius.narendra@mhs.unsoed.ac.id |
| Fardizza Vinda Rahman | Team Member | Sistem Analis | fardizza.rahman@mhs.unsoed.ac.id |
| Adridinan Najmi Faza | Team Member | Programmer | adridinan.faza@mhs.unsoed.ac.id |
| Salman Thufail | Team Member | Programmer | salman.thufail@mhs.unsoed.ac.id |

---

## PROJECT PLANNING

| Bidang Pengetahuan | Proses | Hasil |
|---|---|---|
| **Integrasi** | Rencana Proyek | Proyek direncanakan selama 50 hari. Struktur tahapan:<br>1. Persiapan Project<br>2. Perencanaan<br>3. Pelaksanaan<br>4. Maintenance<br>5. Penutup |
| **Cakupan** | Perencanaan dan Pendefinisian Lingkup Proyek | Detail lingkup proyek:<br>1. Persiapan (Wawancara Medkreminfo, menyusun project charter)<br>2. Perencanaan (Desain database, pembagian tugas)<br>3. Pelaksanaan (Pembuatan Mockup, Programming Back-end & Front-end, Testing)<br>4. Maintenance (Perbaikan bug)<br>5. Penutup (Serah terima sistem ke BEM FT) |
| **Waktu** | Estimasi Penjadwalan | 1. Persiapan Project : 3 Hari<br>2. Perencanaan : 3 Hari<br>3. Pelaksanaan : 30 Hari<br>4. Maintenance : 10 Hari<br>5. Penutup : 4 Hari |
| **Biaya** | Estimasi Biaya | Estimasi biaya infrastruktur dan *man-power* (hipotesis):<br>● Sistem Informasi Rp 6.000.000,00<br>● Infrastruktur (Hosting/Domain) Rp 750.000,00<br>● Total Biaya Rp 6.750.000,00 |
| **SDM** | Akuisisi Staff | Penempatan staf proyek:<br>● Timotius Willy Narendra (PM)<br>● Fardizza Vinda Rahman (Analis)<br>● Adridinan Najmi Faza (Programmer)<br>● Salman Thufail (Programmer) |
| **Resiko** | Identifikasi Resiko | Risiko tertinggi adalah penolakan pengguna (user resistance) dan *scope creep*. Mitigasi dilakukan dengan membuat desain web yang ramah pengguna serta mengunci kesepakatan fitur awal. |
| **Pengadaan** | Perencanaan Pembelian | Rencana pembelian/penyewaan: Layanan *Cloud Hosting* dan *Domain* (.com / .org). |

---

## Scope Statement

**Nama Proyek** : Sistem Informasi Layanan Pemesanan Konten Medkreminfo
**Tanggal** : 7 September 2026

**Dasar Pertimbangan Proyek** :
Proyek ini dimaksudkan untuk menampung dan mengelola seluruh alur pengajuan *brief*, aset, dan jadwal publikasi konten dari 14 kementerian di lingkungan BEM FT secara terpusat. Sistem ini menyediakan dasbor interaktif yang memetakan antrean pengerjaan, alokasi staf pelaksana, status tahapan pengerjaan (*lifecycle ticket*), serta kalender tayang guna menghilangkan tumpang tindih jadwal dan miskomunikasi.

**Kanal Publikasi yang Didukung** :
Sistem mengakomodasi pemesanan untuk empat (4) kanal media publikasi resmi BEM FT:
1. **Instagram Feeds**: Desain poster kegiatan, carousel mikroblog edukasi, dan infografis resmi (format rasio 1:1 atau 4:5).
2. **Instagram Story**: Pengumuman penting, broadcast kegiatan, live report, dan interaksi pengikut (format rasio 9:16).
3. **LinkedIn**: Publikasi profesional, pencapaian prestasi mahasiswa/fakultas, relasi kemitraan/alumni, dan siaran pers kegiatan formal (format visual disertai naskah artikel/copywriting formal).
4. **TikTok**: Konten video pendek vertikal (format 9:16), tren kreatif mahasiswa, dokumentasi recap kegiatan, dan edukasi interaktif (memerlukan lampiran konsep alur dan naskah/script video).

**Karakteristik Produk dan Persyaratan** :
Sistem Informasi ini merupakan aplikasi berbasis *web* yang memiliki modul-modul fungsional utama:
1. **Formulir Pemesanan Konten Terstruktur (Multi-Kanal)**:
   - Kementerian pemesan memilih satu atau beberapa kanal publikasi tujuan (Instagram Feeds, Story, LinkedIn, TikTok).
   - Form menyesuaikan *input requirement* sesuai kanal (misal: rasio dimensi visual, konsep naskah video TikTok, naskah caption formal LinkedIn, lampiran materi/aset, dan tanggal tenggat publikasi).
   - Admin Medkreminfo dapat memvalidasi kelayakan brief, memberikan catatan revisi, atau menyetujui pesanan.
2. **Manajemen Penugasan & Spesialisasi Staf**:
   - Sistem merutekan pesanan ke staf PJ kementerian terkait atau mendistribusikannya ke staf yang memiliki keahlian khusus (misal: editor video untuk TikTok, desainer grafis untuk Feeds/Story).
   - Menteri Medkreminfo (Admin) memiliki wewenang memantau beban kerja (*workload balance*) dan melakukan pengalihan tugas (*re-assign*) bila staf terkait mengalami beban berlebih (*overload*).
3. **Kalender Editorial Publikasi (Editorial Calendar)**:
   - Menampilkan visualisasi jadwal tayang postingan di seluruh kanal (Instagram, LinkedIn, TikTok) agar tidak terjadi bentrok publikasi pada hari dan jam yang sama.
4. **Pelacakan Status & Notifikasi Revisi**:
   - Pelacakan alur tiket transparan dari *Draft*, *Submitted*, *In Progress*, *Review/Revision*, *Ready to Post*, hingga *Published*.
5. **Autentikasi & Hak Akses Berbasis Peran**:
   - Login terverifikasi untuk 3 tingkatan pengguna: Admin (Menteri Medkreminfo), Eksekutor (Staf Medkreminfo), dan Klien (14 Kementerian Pemesan).

**Deliverables (Luaran Proyek)** :
1. Aplikasi Web Sistem Informasi Layanan Pemesanan Konten Medkreminfo siap pakai.
2. Dokumen Analisis dan Desain Sistem (SRS & SDD) serta *Source Code*.
3. Buku Panduan Pengguna (*User Manual*) untuk Admin, Staf Medkreminfo, dan Kementerian Pemesan.
4. Berita Acara Sosialisasi dan Serah Terima Sistem ke Pengurus BEM FT.

**Batasan Proyek (Out of Scope)** :
1. **Tidak Melakukan Auto-Posting**: Sistem tidak terintegrasi secara otomatis via API untuk langsung mengunggah konten ke server Instagram, LinkedIn, atau TikTok. Publikasi akhir ke platform media sosial tetap dilakukan manual oleh staf pengelola akun.
2. **Bukan Software Pengolah Grafis/Video**: Sistem tidak menyediakan antarmuka pengeditan desain atau video di dalam web; pengerjaan karya tetap menggunakan software eksternal (Adobe Photoshop, Illustrator, Premiere, Canva, CapCut).
3. **Tidak Menangani Manajemen Komentar/Interaksi Medsos**: Pengelolaan *direct message* (DM), komentar audiens, dan analisis metrik engagement media sosial berada di luar lingkup sistem ini.
4. **Hanya untuk Lingkup Internal BEM FT**: Sistem hanya melayani kebutuhan kementerian di dalam BEM FT dan tidak dirancang untuk transaksi pemesanan komersial dari pihak sponsor eksternal umum.
