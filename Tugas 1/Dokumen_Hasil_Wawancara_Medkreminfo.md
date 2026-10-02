# DOKUMEN HASIL WAWANCARA DAN ELISITASI KEBUTUHAN (DISCOVERY)
## Sistem Informasi Layanan Pemesanan Konten Medkreminfo BEM FT UNSOED
### Mata Kuliah: IF21307 – Analisis dan Desain Sistem

---

## 1. Berita Acara Wawancara

| Komponen | Rincian Keterangan |
|---|---|
| **Topik Wawancara** | Elisitasi Kebutuhan dan Analisis Alur Kerja *As-Is* Pemesanan Konten Media Sosial Medkreminfo BEM FT |
| **Hari / Tanggal** | Senin, 7 September 2026 |
| **Waktu Pelaksanaan** | 15.30 – 17.00 WIB |
| **Tempat / Lokasi** | Ruang Sekretariat Bersama BEM Fakultas Teknik UNSOED, Gedung Kemahasiswaan Kampus Blater, Purbalingga |
| **Narasumber** | **Aba Ibrahim (Sdr. Baim)** |
| **Jabatan Narasumber** | Staf Kementerian Media, Kreatif, dan Informasi (Medkreminfo) BEM FT UNSOED Periode 2026/2027 |
| **Tim Pewawancara** | 1. **Timotius Willy Narendra** (H1D025052) — Notulis & Moderator<br>2. **Fardizza Vinda Rahman** (H1D025067) — Analis Sistem<br>3. **Adridinan Najmi Faza** (H1D025059) — Pengembang / Pengamat Alur |

---

## 2. Lembar Persetujuan Narasumber (Informed Consent)

Narasumber telah diberikan penjelasan mengenai maksud dan tujuan wawancara ini, yaitu murni untuk keperluan akademik penyusunan spesifikasi kebutuhan perangkat lunak (*Software Requirements Specification* - SRS) pada mata kuliah Analisis dan Desain Sistem di Program Studi S1 Informatika Unsoed. Narasumber menyatakan persetujuannya untuk memberikan keterangan proses kerja internal, pain point yang dialami, serta memberikan izin pencantuman identitas peran dan kutipan dialog di dalam artefak analisis sistem.

*Purbalingga, 7 September 2026*  
**Narasumber Terwawancara,**  

*(ditandatangani)*  

**Aba Ibrahim**  
NIM. Mahasiswa Fakultas Teknik UNSOED

---

## 3. Matriks Pertanyaan Kunci dan Ringkasan Jawaban

| No. | Kode Bukti | Pertanyaan Elisitasi | Ringkasan Jawaban Narasumber |
|---|---|---|---|
| 1 | **W01** | Bagaimana alur pemesanan konten publikasi yang berjalan saat ini dari 14 kementerian lain ke Medkreminfo? | Tidak ada sistem atau portal khusus. Kementerian lain mengirim pesan permohonan secara manual via WhatsApp pribadi staf penanggung jawab (PJ) kementerian atau ke grup WA. Staf Medkreminfo kemudian mencatat brief tersebut secara mandiri di catatan HP atau spreadsheet pribadi. |
| 2 | **W02** | Apa saja kendala atau masalah operasional paling kritis yang sering terjadi dengan alur perpesanan saat ini? | Pesanan sering tenggelam di tumpukan riwayat chat WhatsApp sehingga terlambat atau lupa dikerjakan. Tenggat waktu (*deadline*) sering salah paham karena komunikasi tidak formal. Tidak ada rekam jejak revisi dan kementerian pemesan sering menanyakan status secara berulang. |
| 3 | **W03** | Bagaimana pembagian beban kerja staf di Medkreminfo saat ini dan apakah sudah merata? | Saat ini pembagian staf berbasis PJ per kementerian. Akibatnya beban kerja sangat timpang: staf yang memegang kementerian yang sangat aktif kewalahan menerima banyak tugas bersamaan, sementara staf yang memegang kementerian pasif tidak memiliki pekerjaan. Selain itu, staf kadang tidak tahu siapa yang mengambil pekerjaan tertentu sehingga terjadi tumpang tindih. |
| 4 | **W04** | Berapa rata-rata volume permohonan konten yang masuk setiap minggunya? | Pada kondisi normal berkisar antara 5 hingga 10 permohonan per minggu. Namun pada periode puncak acara besar (dies natalis, inaugurasi, pemilu mahasiswa), lonjakan dapat mencapai 15 hingga 20 permohonan dalam satu minggu. |
| 5 | **W05** | Apakah sebelumnya pernah dicoba sistem atau alat bantu manajemen tugas digital? | Pernah mencoba menggunakan platform Trello, tetapi gagal dipertahankan karena banyak staf enggan login ulang, antarmuka terasa rumit, dan tidak ada admin yang mengelola alur secara konsisten. Narasumber sangat menginginkan sistem web baru yang simpel, ringan, dan nyaman diakses langsung dari ponsel (*smartphone*). |
| 6 | **W06** | Kanal publikasi resmi apa saja yang dikelola dan bagaimana tren pemesanannya? | 4 kanal utama: Instagram Feeds (paling dominan, berupa poster/carousel), Instagram Story (live report & pengumuman cepat), LinkedIn (siaran pers & kemitraan), dan TikTok (konten video kreatif). Sering terjadi kesalahan kirim ukuran rasio gambar dari pemesan antar kanal tersebut. |
| 7 | **W07** | Siapa saja pihak yang terlibat dalam tata kelola alur kerja pesanan konten? | Terdapat 3 pihak: Klien (pengurus 14 kementerian pemesan), Admin (Menteri/Sekretaris Medkreminfo sebagai kurator/penugas), dan Eksekutor (staf teknis desainer grafis, editor video, atau copywriter). |
| 8 | **W08** | Bagaimana mekanisme revisi hasil desain/video yang terjadi di lapangan? | Saat ini revisi tidak memiliki batasan kuota. Sering terjadi satu poster direvisi hingga 4–5 kali untuk perubahan-perubahan kecil yang berulang sehingga sangat melelahkan staf eksekutor dan menunda konten kementerian lain. |

---

## 4. Transkrip Lengkap Percakapan Wawancara (Verbatim Transcript)

> **Keterangan Penutur:**  
> **T** = Timotius Willy Narendra (Moderator / PM)  
> **F** = Fardizza Vinda Rahman (Sistem Analis)  
> **A** = Adridinan Najmi Faza (Programmer)  
> **B** = Aba Ibrahim / Baim (Narasumber Staf Medkreminfo)  

**T (Timotius):** Halo Baim, terima kasih banyak sudah meluangkan waktu sore ini untuk wawancara proyek ADS kami. Boleh ceritakan dulu alur bagaimana kementerian lain di BEM FT memesan konten ke Medkreminfo saat ini?

**B (Aba Ibrahim):** `[W01]` Jadi sekarang tuh jujur belum ada sistem khusus sama sekali. Kalau kementerian lain di BEM butuh poster atau publikasi proker, mereka biasanya langsung chat ke grup WhatsApp Medkreminfo, atau yang paling sering malah langsung chat ke nomor WhatsApp pribadiku atau ke Pak Menteri. Terus dari chat itu, kami catat sendiri di catatan HP atau spreadsheet pribadi masing-masing.

**T (Timotius):** Berarti murni lewat chat WhatsApp ya Baim? Tidak ada formulir baku seperti Google Forms atau sejenisnya?

**B (Aba Ibrahim):** `[W01]` `[W05]` Iya, murni WhatsApp. Dulu pernah sih kita coba pakai Trello biar lebih rapi, tapi nggak jalan. Anak-anak staf males kalau harus login-login lagi di browser desktop, terus nggak ada yang ngurusin secara terpusat, jadi akhirnya mati sendiri. Ujung-ujungnya semua balik lagi ke chat WA karena dianggap paling instan.

**F (Fardizza):** Nah dari alur WhatsApp yang berjalan itu, seberapa sering pesanan konten masuk dalam kurun waktu satu minggu, Baim?

**B (Aba Ibrahim):** `[W04]` Normalnya seminggu itu bisa masuk 5 sampai 10 request. Tapi kalau lagi musim proker besar, kayak Dies Natalis FT, Techno, atau masa pemilu BEM, itu bisa membludak sampai 15 sampai 20 lebih per minggu. Itu masa-masa paling chaos buat anak-anak Medkrem.

**A (Adridinan):** Di masa-masa sibuk seperti itu, masalah apa saja yang paling sering muncul dan bikin pusing tim Medkreminfo?

**B (Aba Ibrahim):** `[W02]` `[W03]` Banyak banget masalahnya. Yang nomor satu itu request sering tenggelam di tumpukan chat WA. Tahu sendiri kan grup WA BEM itu ramai banget, jadi pesan brief dari menteri lain ketumpuk, terus kelupaan dikerjain. Masalah kedua, deadline sering miskomunikasi. Kadang kementerian pemesan merasa sudah minta dari kemarin, tapi staf kami ngerasa baru di-chat kemarin sore. Terus staf juga bingung, tugas ini sebenarnya siapa yang megang, jadi kadang tugasnya dobel dikerjain atau malah nggak ada yang ngerjain sama sekali.

**F (Fardizza):** Soal pembagian staf itu menarik Baim, bagaimana sistem penugasan staf Medkreminfo saat ini?

**B (Aba Ibrahim):** `[W03]` Sekarang tuh sistemnya PJ (Penanggung Jawab). Jadi tiap staf Medkrem ditempelin jadi PJ buat 1 atau 2 kementerian. Nah masalahnya, keaktifan kementerian itu beda-beda jauh. Ada kementerian yang prokernya rajin banget tiap minggu minta poster, otomatis staf yang jadi PJ di situ kelabakan dan begadang terus. Tapi ada kementerian yang pasif, jadi PJ-nya santai nggak ada kerjaan. Nggak ada sistem yang bisa bagi beban kerja secara adil atau ngalihin tugas kalau ada staf yang lagi sakit.

**A (Adridinan):** Terus untuk jenis kontennya sendiri, biasanya kanal publikasi apa yang paling banyak diminta?

**B (Aba Ibrahim):** `[W06]` Instagram Feeds jelas paling banyak, hampir tiap hari ada poster pengumuman atau ucapan. Terus Instagram Story buat live report dan info cepat. LinkedIn sama TikTok mulai sering, terutama TikTok sekarang banyak video rekap kegiatan. Nah, kendalanya kementerian pemesan sering ngawur ngasih materi. Misal minta dibuatin Story tapi ngasih fotonya rasio kotak 1:1, jadinya kalau dipaksakan ke Story 9:16 posternya kepotong jelek.

**T (Timotius):** Kalau soal proses revisi bagaimana Baim? Apakah ada aturan batasannya?

**B (Aba Ibrahim):** `[W08]` Nah ini juga penyakit lama. Nggak ada batasan revisi. Sering banget desainer kami sudah capek-capek bikin poster, terus kementerian pemesan bolak-balik minta ganti warna font, geser logo dikit, sampai 4 atau 5 kali revisi kecil. Akhirnya staf kami burnout, padahal masih banyak antrean poster dari kementerian lain yang nunggu. Harusnya dibatasi maksimal dua kali revisi minor aja cukup.

**T (Timotius):** Terakhir Baim, kalau kami bangunkan sistem informasi berbasis web untuk Medkreminfo, apa ekspektasi dan fitur utama yang paling Baim harapkan?

**B (Aba Ibrahim):** `[W05]` `[W07]` Yang paling utama: tolong buat sistemnya simpel dan nyaman dibuka lewat HP. Jangan ribet bikin staf malas login. Kedua, kementerian pemesan bisa langsung isi form lengkap beserta asetnya, dan mereka bisa lihat sendiri progresnya sudah sampai mana tanpa perlu nanya-nanya ke WA lagi. Ketiga, ada Menteri yang bisa mantau semua tiket dan bagi tugas ke staf secara adil. Kalau tiga hal itu beres, alur kerja Medkreminfo bakal jauh lebih tenang dan teratur.

**T (Timotius):** Baik, poin-poinnya sangat jelas dan komprehensif sekali. Terima kasih banyak atas waktunya ya Baim!

---

## 5. Matriks Kodifikasi Temuan & Pemetaan Pain Point

Dari transkrip wawancara di atas, seluruh data disintesis menjadi tabel temuan elisitasi yang terhubung ke dokumen spesifikasi kebutuhan sistem (SRS):

| Kode Bukti | Sumber Bukti | Pernyataan Temuan Lapangan | Masalah / Pain Point (PP) | Implikasi Kebutuhan Sistem Terkait |
|---|---|---|---|---|
| **W01** | Wawancara Baim (Tanya 1) | Pemesanan via chat WhatsApp pribadi ke PJ kementerian dan pencatatan manual di notes pribadi. | **PP-01:** Permintaan tidak terstandarisasi, data brief tercecer dan rawan hilang. | **FR-02:** Formulir terstruktur multi-kanal terpusat.<br>**FR-04:** Penyimpanan aset materi terpadu. |
| **W02** | Wawancara Baim (Tanya 2) | Pesanan tenggelam di chat WA, deadline sering salah paham, pemesan berulang kali menanyakan status. | **PP-01:** Ketiadaan transparansi dan ketidakjelasan batas waktu pengerjaan. | **FR-03:** Validasi batas waktu minimum (SLA BR-01).<br>**FR-05:** Pelacakan status pengerjaan tiket mandiri bagi Klien. |
| **W03** | Wawancara Baim (Tanya 3) | Beban kerja staf tidak merata karena sistem PJ kementerian pasif vs aktif; staf tidak tahu siapa yang mengambil pekerjaan. | **PP-02:** Ketimpangan beban kerja (*workload imbalance*) dan ketiadaan visibilitas penugasan. | **FR-06:** Dasbor manajemen tiket masuk Admin.<br>**FR-08:** Alokasi tugas berbasis beban aktif staf.<br>**FR-09:** Pengalihan tugas saat overload (BR-03, BR-04). |
| **W04** | Wawancara Baim (Tanya 4) | Volume request normal 5–10 per minggu, melonjak hingga 15–20 per minggu saat agenda dies natalis/acara besar. | **PP-01:** Beban antrean manual memicu kelambatan operasional organisasi. | **NFR-PERF-02:** Skalabilitas antrean concurrent user.<br>**FR-14:** Kalender editorial publikasi terpadu. |
| **W05** | Wawancara Baim (Tanya 5) | Trello ditinggalkan karena sulit dan tidak nyaman; menginginkan sistem web yang simpel dan ramah diakses lewat ponsel. | **PP-01:** Resistensi adopsi alat bantu digital yang kompleks (*user resistance*). | **NFR-PORT-01:** Antarmuka responsif mobile 360px.<br>**NFR-USE-01:** Waktu pengisian form singkat (≤ 5 menit). |
| **W06** | Wawancara Baim (Tanya 6) | Kesalahan format rasio gambar (misal materi 1:1 dipaksakan untuk tayang di Story 9:16). | **PP-03:** Miskomunikasi spesifikasi teknis dimensi antar-kanal media sosial. | **FR-02:** Formulir adaptif yang mengunci aturan dimensi kanal publikasi sejak awal input. |
| **W07** | Wawancara Baim (Tanya 7) | Tata kelola melibatkan 3 aktor: Klien pemesan, Menteri sebagai validator/assignor, dan Eksekutor staf fungsional. | **PP-02:** Ketiadaan pembagian peran yang baku dalam alur persetujuan karya. | **FR-01:** Role-Based Access Control (RBAC 3 level).<br>**FR-07:** Fitur persetujuan/penolakan brief oleh Admin. |
| **W08** | Wawancara Baim (Tanya 8) | Revisi berulang hingga 4–5 kali untuk perubahan minor yang melelahkan staf pelaksana. | **PP-04:** Ketiadaan kuota batasan revisi memicu kelelahan staf (*burnout*). | **FR-12:** Batasan kuota maksimal 2 kali revisi minor (BR-02).<br>**FR-13:** Fitur persetujuan akhir resmi (Final Approve). |

---

## 6. Ringkasan Kesimpulan Elisitasi

Berdasarkan triangulasi bukti wawancara bersama narasumber Sdr. Aba Ibrahim, dapat disimpulkan bahwa permasalahan utama di Medkreminfo BEM FT bukan terletak pada kurangnya staf kreatif, melainkan pada **ketiadaan sistem kerja terpusat (*ticketing & workflow management*)**. 

Solusi perangkat lunak yang dirancang harus fokus pada empat pilar:
1. **Standarisasi Formulir Pemesanan**: Mengeliminasi pesanan via chat personal dengan form adaptif multi-kanal.
2. **Keadilan Alokasi Tugas**: Membantu Menteri membagi tugas secara transparan berdasarkan kapasitas aktif staf pelaksana (*workload balancing*).
3. **Kepastian SLA & Kontrol Revisi**: Menegakkan batasan waktu pengajuan konten dan membatasi revisi minor maksimal 2 kali.
4. **Visibilitas dan Transparansi**: Menyediakan pelacakan status tiket langsung bagi kementerian pemesan dan kalender editorial penayangan terpadu.
