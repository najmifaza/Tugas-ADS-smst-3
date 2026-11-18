# LAPORAN TUGAS MANDIRI PERTEMUAN 10 – PEMODELAN DATA
## IF21307 Analisis dan Desain Sistem

---

### IDENTITAS MAHASISWA & PROYEK
* **Nama Lengkap:** Adridinan Najmi Faza
* **NIM:** H1D025059
* **Peran Tim:** Pengembang Perangkat Lunak
* **Nama Tim:** Kelompok Proyek BEM FT Medkreminfo
* **Anggota Tim:**
  1. Timotius Willy Narendra (H1D025052) — Project Manager
  2. Fardizza Vinda Rahman (H1D025067) — Analis Sistem
  3. Adridinan Najmi Faza (H1D025059) — Pengembang Perangkat Lunak
  4. Salman Thufail (H1D022109) — Pengembang Perangkat Lunak
* **Judul Proyek:** Sistem Informasi Layanan Pemesanan Konten Medkreminfo BEM FT UNSOED
* **Use Case Analisis:** UC-01: Pengajuan Tiket Request Konten (Klien)

---

### BAGIAN A. USE CASE NARRATIVE (ANALISIS KATA BENDA & KATA KERJA)

> **Keterangan Notasi:**
> * Kata benda pemodelan dicetak **tebal** (**bold**) sebagai kandidat entitas atau atribut.
> * Kata kerja dicetak *miring* (*italic*) sebagai kandidat relasi.

#### UC-01: Pengajuan Tiket Request Konten (Klien)
* **Aktor Utama:** **Klien** (Perwakilan Kementerian BEM FT)
* **Kebutuhan Terkait:** FR-02, FR-03, FR-04, BR-01, BR-05
* **Precondition:** **Pengguna** terautentikasi akun Klien.
* **Trigger:** Klien *memilih* menu Buat Pesanan Konten Baru.

##### Alur Utama (Main Flow):
1. Klien *membuka* **halaman formulir pemesanan konten**.
2. Klien *mengisi* **judul publikasi**, *memilih* **kanal tujuan** (Instagram Feeds, Story, LinkedIn, TikTok), dan *menentukan* **tanggal target tayang**.
3. Sistem *memverifikasi* selisih hari tanggal tayang terhadap **aturan SLA** (BR-01).
4. Klien *mengunggah* **berkas materi pendukung** (gambar, dokumen, video) atau *menyematkan* **tautan Google Drive**, serta *mengisi* **deskripsi brief naskah**.
5. Klien *menekan* tombol kirim permohonan.
6. Sistem *memvalidasi* isian formulir dan *menerima* berkas aset pendukung (termasuk video > 50 MB sesuai BR-05).
7. Sistem *menerbitkan* **ID tiket unik** (#MED-YYYYMM-XXX), *menyimpan* **data tiket** berstatus Submitted, dan *mengirimkan* notifikasi konfirmasi.

##### Alur Alternatif & Pengecualian:
* **3a. Pengajuan Mendadak (< Batas Hari SLA):** Sistem *menampilkan* peringatan SLA (BR-01). Klien *mengisi* **alasan kebutuhan darurat**, tiket diberi penanda **Rush Order**, lalu alur berlanjut ke langkah 4.
* **6a. Format Berkas Tidak Didukung:** Sistem *menolak* berkas & *menampilkan* pesan galat. Pengguna *memilih* berkas pengganti yang valid atau *menyematkan* tautan penyimpanan awan.
* **Postcondition:** **Tiket** *tercatat* pada basis data dengan status Submitted dan muncul di antrean verifikasi Admin.

---

### BAGIAN B. TABEL SARING KANDIDAT

| No | Kandidat | Keputusan | Alasan |
|---|---|---|---|
| 1 | Klien / Perwakilan Kementerian | Entitas PENGGUNA | Aktor pembuat pesanan. Ada 14 kementerian pemesan dan staf Medkreminfo. Datanya disimpan lengkap (nama, email, password, peran, kontak, spesialisasi) sesuai FR-01. |
| 2 | Halaman formulir pemesanan | Bukan entitas | Komponen antarmuka (UI) input di peramban. Nilai isian formulir disimpan ke dalam tabel tiket pesanan. |
| 3 | Tiket / Data tiket | Entitas TIKET_PESANAN | Objek data transaksional utama yang disimpan dan dilacak status pengerjaannya dari pengajuan hingga rilis media sosial. |
| 4 | ID tiket (#MED-YYYYMM-XXX) | Atribut TIKET_PESANAN | Kunci utama (Primary Key) penanda unik tiap pesanan agar tidak tertukar sesuai spesifikasi FR-02. |
| 5 | Judul publikasi | Atribut TIKET_PESANAN | Topik atau nama publikasi konten yang diajukan oleh kementerian pemesan. |
| 6 | Kanal tujuan | Atribut TIKET_PESANAN | Pilihan media tayang (Feeds, Story, LinkedIn, TikTok) penentu batas hari SLA pengerjaan di aturan BR-01. |
| 7 | Tanggal target tayang | Atribut TIKET_PESANAN | Batas tanggal publikasi konten yang diharapkan oleh pemesan. |
| 8 | Selisih hari / Validasi SLA | Bukan entitas | Hasil perhitungan dinamis (tanggal tayang dikurangi tanggal pesan). Divalidasi runtime sesuai aturan bisnis BR-01 tanpa disimpan ke tabel tersendiri. |
| 9 | Berkas materi / Aset pendukung | Entitas BERKAS_ASET | Berkas materi produksi (foto, video mentahan, naskah). Satu pesanan dapat memiliki banyak berkas dengan batas retensi simpan sesuai BR-05. |
| 10 | Tautan Google Drive | Atribut BERKAS_ASET | Tautan cadangan penyimpanan awan jika berkas video mentahan berukuran besar (>50 MB). |
| 11 | Deskripsi brief naskah | Atribut TIKET_PESANAN | Catatan arahan konsep, narasi, dan salinan teks yang diminta pemesan. |
| 12 | Status tiket (Submitted) | Atribut TIKET_PESANAN | Status tahapan kerja tiket (Submitted, In Progress, Review, Published) untuk pelacakan alur kerja. |
| 13 | Alasan kebutuhan darurat | Atribut TIKET_PESANAN | Keterangan justifikasi dispensasi yang wajib diisi jika kementerian memesan melewati batas SLA. |
| 14 | Label Rush Order | Atribut TIKET_PESANAN | Penanda boolean (is_rush_order) penentu prioritas antrean pesanan darurat. |
| 15 | Tombol kirim / Pesan galat | Bukan entitas | Elemen interaksi visual dan respon validasi pada layar. Tidak memerlukan persistensi data pada sistem basis data. |
| 16 | Notifikasi konfirmasi | Bukan entitas | Pesan pemberitahuan status transaksi. Pada cakupan versi awal belum dipetakan ke tabel log riwayat notifikasi. |

---

### BAGIAN C. ERD V1 SELURUH SISTEM & LEGENDA

#### 1. Diagram ERD v1 (Notasi Crow's Foot)
*(Diagram visual horizontal monokrom terlampir pada dokumen laporan)*

#### 2. Legenda Notasi (Crow's Foot)
* `||--o{` : One-to-Many Optional (induk 1 dapat memiliki nol atau banyak data anak).
* `||--||` : One-to-One Mandatory (induk 1 berpasangan tepat dengan 1 data anak).
* `|o--o{` : Zero-or-One to Many Optional (anak dapat berstatus tanpa data induk / belum ditugaskan eksekutor).
* `PK` : *Primary Key* (kolom identitas unik entitas).
* `FK` : *Foreign Key* (kunci relasi penghubung antar tabel).

#### 3. Asal Entitas di Luar Use Case UC-01
1. **KEMENTERIAN** (Deskripsi 1.2, NFR-SEC-02, W01): Memisahkan kepemilikan data pesanan antar 14 kementerian di lingkungan BEM FT.
2. **DRAF_KARYA** (FR-11, UC-03): Menampung riwayat berkas pratinjau desain karya (v1, v2) yang diunggah staf pelaksana.
3. **RIWAYAT_REVISI** (FR-12, BR-02, UC-04): Menyimpan catatan perbaikan dari klien dengan pembatasan kuota maksimal 2 kali siklus revisi minor.
4. **PUBLIKASI_KONTEN** (FR-15, UC-05): Mencatat tautan resmi publikasi medsos, tanggal tayang riil, serta identitas staf yang menerbitkan konten.

---

### BAGIAN D. TABEL BUKTI RELASI

| No | Relasi (Entitas – Kata Kerja – Entitas) | Card. | Kutipan Bukti dan ID (FR/BR) | Jika Tidak Ada Bukti: Pertanyaan Stakeholder |
|---|---|---|---|---|
| 1 | KEMENTERIAN – menaungi – PENGGUNA | 1 : N | Sebagian. NFR-SEC-02: "Klien dilarang mengakses/mengedit berkas & tiket kementerian lain..." dan Bab 1.2: 14 kementerian di lingkungan BEM FT. Sisi 1 akun terikat ke kementerian; sisi N dari struktur organisasi. | Apakah satu kementerian boleh memiliki lebih dari satu akun perwakilan pengurus? |
| 2 | PENGGUNA (Klien) – mengajukan – TIKET_PESANAN | 1 : N | Lengkap. FR-02: Klien membuat tiket baru melalui formulir terstruktur, dan FR-05: menampilkan riwayat tiket milik Klien. Satu akun klien membuat banyak pesanan (N), tiap tiket dibuat tepat 1 klien (1). | – |
| 3 | PENGGUNA (Eksekutor) – mengerjakan – TIKET_PESANAN | 0..1 : N | Lengkap. BR-04: Eksekutor maksimal memegang 3 tiket aktif In Progress, dan FR-08: Admin menugaskan eksekutor ke tiket disetujui. Relasi 0..1 karena saat tiket baru diajukan, eksekutor masih kosong. | – |
| 4 | TIKET_PESANAN – memiliki – BERKAS_ASET | 1 : N | Lengkap. FR-04: Pengguna mengunggah/mengunduh berkas aset pendukung (gambar, naskah, video >50MB) selama produksi, dan BR-05: aset disimpan selama tiket aktif. Satu tiket memuat banyak berkas (N). | Berapa batas maksimal jumlah berkas aset yang boleh diunggah dalam satu tiket? |
| 5 | TIKET_PESANAN – menghasilkan – DRAF_KARYA | 1 : N | Lengkap. FR-11: Eksekutor memperbarui status In Progress dan mengunggah berkas/tautan draf karya (v1, v2) untuk ditinjau pemesan. Satu tiket pesanan dapat menghasilkan beberapa versi draf. | – |
| 6 | TIKET_PESANAN – menerima – RIWAYAT_REVISI | 1 : N | Lengkap. FR-12: Klien mengajukan catatan revisi minor maksimal 2 kali siklus, dan BR-02: pembatasan kuota maksimal 2 siklus revisi minor per tiket pesanan. Poin revisi ditautkan ke tiket terkait. | – |
| 7 | TIKET_PESANAN – diterbitkan pada – PUBLIKASI_KONTEN | 1 : 1 | Lengkap. FR-15: Staf sosmed memasukkan tautan (URL) rilis medsos, otomatis mengubah status menjadi Published & mencatat tanggal tayang aktual. Satu tiket berpasangan tepat 1 publikasi. | – |
| 8 | PENGGUNA (Staf) – mempublikasikan – PUBLIKASI_KONTEN | 1 : N | Lengkap. FR-15 dan alur UC-05: Staf publikasi mencatatkan tautan rilis resmi ke sistem. Satu staf sosmed dapat mempublikasikan banyak konten pesanan dari berbagai kementerian. | – |

---

### BAGIAN E. REFLEKSI

1. **Bagian ERD mana yang paling diragukan, dan mengapa?**  
   Pemisahan entitas PUBLIKASI_KONTEN dari TIKET_PESANAN. Relasi keduanya bernilai 1 : 1, di mana satu tiket pesanan yang selesai dikerjakan menghasilkan tepat satu catatan publikasi. Keputusan ini sempat diragukan karena datanya dapat dilebur menjadi kolom atribut pada tabel pesanan (url_publikasi dan tanggal_terbit). Namun pemisahan tabel tetap dipilih agar pencatatan waktu siar aktual dan staf media sosial pelaksana (id_staf_medsos) terisolasi secara terstruktur dari alur produksi internal tim kreatif.

2. **Keputusan apa yang diambil berdasarkan tebakan, bukan dokumen?**  
   Menautkan entitas RIWAYAT_REVISI langsung ke TIKET_PESANAN (bukan ke DRAF_KARYA). Di dalam SRS diatur batas kuota maksimal 2 kali revisi minor per tiket pesanan (BR-02), sehingga kuota dan catatan koreksi ditautkan langsung ke tiket induk. Namun pada alur kerja nyata, masukan revisi biasanya merujuk spesifik pada berkas versi draf tertentu (misalnya draf v1). Karena dokumen kebutuhan belum mendefinisikan relasi langsung antara revisi dan nomor draf, relasi langsung ke tiket diambil sebagai asumsi penyederhanaan rancangan awal.

3. **Data apa yang mungkin dibutuhkan sistem tetapi belum ada di ERD?**  
   Tabel pencatatan riwayat perpindahan status tiket (audit trail perubahan status dari Submitted, Disetujui/Ditolak Admin, Assigned, In Progress, Review, hingga Published). Saat ini status tiket hanya tersimpan sebagai nilai tunggal terbaru pada kolom status_tiket. Jika terjadi penolakan brief oleh Menteri atau pengalihan tugas antar staf, riwayat alasan dan stempel waktu perubahannya belum tercatat historis. Selain itu, sistem juga belum memiliki struktur tabel log untuk merekam riwayat pengiriman notifikasi pengingat publikasi ke pengguna.
