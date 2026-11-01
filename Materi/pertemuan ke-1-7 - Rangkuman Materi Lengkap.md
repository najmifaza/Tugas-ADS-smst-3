# DOKUMENTASI LENGKAP MATERI KULIAH ANALISIS DAN DESAIN SISTEM (IF21307)
**Program Studi Informatika — Universitas Jenderal Soedirman**  
**Cakupan:** Pertemuan 01 s.d. Pertemuan 07 (Fase Discovery hingga SRS Baseline v1.0)  
**Bobot & Kurikulum:** 3 SKS | Kurikulum 2024 / Versi Materi Final 1.0 (2026)  
**Landasan Standar Global:** ISO/IEC/IEEE 29148:2018, ISO/IEC 25010:2023, OMG UML 2.5.1, OMG BPMN 2.0.2, NIST SSDF 1.1, OWASP ASVS 5.0.0, Scrum Guide 2020, CS2023.

---

## DAFTAR ISI
1. [Pertemuan 01: Fondasi Sistem, Sistem Informasi, dan Peran Analis](#pertemuan-01-fondasi-sistem-sistem-informasi-dan-peran-analis)
2. [Pertemuan 02: Project Charter dan Analisis Awal](#pertemuan-02-project-charter-dan-analisis-awal)
3. [Pertemuan 03: Teknik Elicitation, Etika, Consent, dan Triangulasi Bukti](#pertemuan-03-teknik-elicitation-etika-consent-dan-triangulasi-bukti)
4. [Pertemuan 04: Sintesis Temuan Analisis (Affinity Mapping, RCA, As-Is, Pain Point, Opportunity)](#pertemuan-04-sintesis-temuan-analisis)
5. [Pertemuan 05: Requirements Engineering (FR, NFR, Business Rules, Acceptance Criteria, RTM, Draft SRS)](#pertemuan-05-requirements-engineering)
6. [Pertemuan 06: Pemodelan Proses Bisnis BPMN 2.0.2 (As-Is ke To-Be, Exception, Design Critique)](#pertemuan-06-pemodelan-proses-bisnis-bpmn-202)
7. [Pertemuan 07: Use Case, Activity Diagram, dan Pembekuan SRS Baseline](#pertemuan-07-use-case-activity-diagram-dan-pembekuan-srs-baseline)
8. [Matriks Integrasi Alur Artefak & Penilaian Akademik](#matriks-integrasi-alur-artefak--penilaian-akademik)

---

# PERTEMUAN 01: FONDASI SISTEM, SISTEM INFORMASI, DAN PERAN ANALIS

### 1. Orientasi Analisis & Desain Sistem
* **Esensi Mata Kuliah:** Studi sistematis terhadap masalah organisasi dan perumusan kebutuhan berbasis bukti (*evidence-based*) guna membangun keputusan desain yang akuntabel (*accountable*).
* **Pergeseran Paradigma:** Fokus beralih dari sekadar "apa yang ingin dibangun (fitur teknis)" menjadi "mengapa perubahan dibutuhkan dan bagaimana alur kerja organisasi berjalan".
* **Metode Project-Based Learning (PBL):** Pengembangan artefak mahasiswa dilakukan terpadu dari *Discovery* $\to$ *Analysis Models* $\to$ *Software Requirements Specification (SRS)* $\to$ *Software Design Description (SDD)* & *Mockup Fungsional* $\to$ *Design Defense*.
* **Batas Pembelajaran:** Bukan *full coding* aplikasi, melainkan penguasaan siklus hidup artefak kebutuhan dan desain secara komprehensif.

### 2. Elemen Dasar & Kerangka Kerja Sistem
* **Definisi Sistem:** Sekumpulan elemen yang saling berhubungan, berinteraksi, dan bekerja sama menuju pencapaian tujuan bersama secara terintegrasi.
* **Elemen Dasar:**
  * **Input:** Data atau sumber daya yang diterima sistem dari lingkungan.
  * **Proses:** Transformasi atau serangkaian aktivitas yang mengubah input menjadi hasil nyata.
  * **Output:** Hasil akhir yang diproduksi oleh proses.
* **Komponen Pelengkap Struktural:**
  * **Batasan (*Boundary*):** Garis pemisah antara elemen internal yang berada dalam kendali sistem dan elemen eksternal di luar kendali langsung. Menentukan cakupan tanggung jawab solusi.
  * **Lingkungan (*Environment*):** Segala hal di luar batasan sistem yang memengaruhi operasional (input, kondisi pasar, regulasi) atau menerima dampak output sistem.
  * **Kontrol (*Control*):** Mekanisme pemandu yang menjaga agar pengoperasian sistem selalu selaras dengan sasaran yang ditetapkan.
  * **Umpan Balik (*Feedback*):** Informasi evaluasi performa output yang dialirkan kembali untuk mendeteksi deviasi/penyimpangan terhadap standar kerja.
* **Siklus Stabilitas Sistem:**
  $$\text{Input \& Proses} \longrightarrow \text{Output} \longrightarrow \text{Umpan Balik} \longrightarrow \text{Analisis Deviasi} \longrightarrow \text{Implementasi Kontrol Iterasi Berikutnya}$$

### 3. Sistem Informasi sebagai Sistem Sosioteknis
* **Sistem vs Sistem Informasi:** Tidak setiap sistem adalah sistem informasi. Sistem tidak wajib berbasis digital (contoh: pengelolaan formulir manual). Transformasi manual ke digital terjadi saat pengelolaan data dilakukan secara terstruktur untuk mendukung operasi dan pengambilan keputusan strategis.
* **5 Komponen Sosioteknis Sistem Informasi:**
  1. **Manusia (*People*):** Pengguna akhir, operator, analis, manajemen.
  2. **Proses (*Process*):** Prosedur, SOP, dan alur kerja data.
  3. **Data (*Data*):** Fakta mentah, informasi terstruktur, dan wawasan bisnis.
  4. **Teknologi (*Technology*):** Perangkat keras (HW), perangkat lunak (SW), jaringan telekomunikasi.
  5. **Kontrol (*Control*):** Tata kelola keamanan, otorisasi akses, dan integritas data.
* **Dampak Ketidakselarasan:** Sistem informasi berisiko gagal total secara bisnis meskipun perangkat lunak berfungsi 100% sempurna secara teknis, apabila terjadi resistensi manusia atau manipulasi data yang keliru.

### 4. Peran Strategis & Tanggung Jawab Analis Sistem
* **Peran Utama:** Jembatan domain (*domain translator*) yang menghubungkan kebutuhan bisnis stakeholder dengan kapabilitas teknis pengembang secara transparan.
* **6 Tanggung Jawab Utama Analis Sistem:**
  1. *Menggali Masalah:* Mengidentifikasi akar masalah mendasar, bukan sekadar mencatat gejala keluhan.
  2. *Memetakan Stakeholder:* Mengidentifikasi semua pihak yang memengaruhi dan terdampak sistem.
  3. *Menerapkan Teknik Elisitasi:* Memilih dan mengeksekusi metode pengumpulan bukti kebutuhan yang tepat.
  4. *Merumuskan Kebutuhan:* Menyusun spesifikasi kebutuhan yang jelas, tidak ambigu, dan dapat diuji.
  5. *Memvalidasi Artefak:* Menjamin keabsahan, kelengkapan, dan konsistensi dokumen di setiap fase.
  6. *Menjaga Keterlacakan (*Traceability*):* Mengawal benang merah logis dari masalah awal hingga rancangan solusi desain.
* **Etika & Komunikasi Profesional:**
  * Penggunaan data hanya sesuai izin dan konteks (*consent*).
  * Menjaga integritas dengan hanya merancang fitur yang memberikan nilai bisnis nyata (*real business value*).

### 5. Memahami Akar Masalah vs Permintaan Solusi Prematur
* **Perangkap Solusi Prematur:** Stakeholder sering langsung meminta solusi teknologi (misal: "Buatkan aplikasi mobile").
* **Tindakan Analis:** Menerapkan *Systems Thinking* dan *Root Cause Analysis* (RCA). Menyelidiki "apa" dan "mengapa" alur kerja bermasalah sebelum menyetujui "bagaimana" bentuk teknologi solusinya.

### 6. Pengantar Siklus Hidup Pengembangan Sistem (SDLC)
* **Definisi SDLC:** Struktur sistematis untuk mengelola transformasi dari kebutuhan pengguna menjadi solusi sistem informasi yang terukur.
* **Model SDLC:**
  * **Prediktif (Linear / Sekuensial):** Fase dijalankan berurutan (Analisis $\to$ Desain $\to$ Koding $\to$ Pengujian $\to$ Deployment). Sangat terstruktur, kaku terhadap perubahan, cocok jika ruang lingkup sudah stabil sejak awal.
  * **Adaptif (Iteratif & Agile):** Mengulang siklus secara bertahap, merilis inkremen kecil yang berfungsi cepat, adaptif terhadap umpan balik dinamis.
  * **Hibrida:** Menggabungkan perencanaan baseline spesifikasi formal di awal dengan implementasi modular bertahap (Agile).

### 7. Dualitas Artefak Kunci: SRS vs SDD & Traceability
* **Software Requirements Specification (SRS):**
  * Menjawab **"APA (*WHAT*)"** yang harus disediakan sistem, batasan operasional, dan atribut kualitas.
  * Memuat: Kebutuhan Fungsional (FR), Kebutuhan Non-Fungsional (NFR), Aturan Bisnis (*Business Rules*), dan Kriteria Penerimaan (*Acceptance Criteria*).
  * Kriteria Kualitas SRS: Tidak Ambigu & Jelas, Dapat Diuji (*Testable*), Berbasis Bukti Discovery (*Evidence-based*).
* **Software Design Description (SDD):**
  * Menjawab **"BAGAIMANA (*HOW*)"** kebutuhan direalisasikan pada tingkat arsitektur logis.
  * Memuat: Desain modul, aliran data, kontrol akses, arsitektur database, dan *mockup antarmuka*.
  * Keputusan desain wajib disertai dasar alasan teknis (*design rationale*).
* **Mekanisme Traceability:**
  $$\text{Req ID (SRS)} \longleftrightarrow \text{Model Analisis} \longleftrightarrow \text{Elemen Desain (SDD)} \longleftrightarrow \text{Verifikasi/Uji}$$

---

# PERTEMUAN 02: PROJECT CHARTER DAN ANALISIS AWAL

### 1. Pembingkaian Masalah Berbasis Bukti (*Problem Framing*)
* **Prinsip Utama:** Proyek berakar dari masalah atau peluang nyata yang terbukti secara faktual, bukan sekadar keinginan membangun aplikasi baru.
* **5 Komponen Inti Problem Statement:**
  1. **Konteks (*Context*):** Latar belakang operasional organisasi saat ini.
  2. **Bukti (*Evidence*):** Fakta pendukung yang dapat diverifikasi (data waktu tunggu, tumpukan berkas fisik, frekuensi keluhan).
  3. **Dampak (*Impact*):** Kerugian operasional, finansial, atau risiko sistem akibat masalah tersebut.
  4. **Pihak Terdampak (*Stakeholders*):** Siapa saja yang mengalami kerugian langsung maupun tidak langsung.
  5. **Pertanyaan Pengarah (*Guiding Question*):** Arah investigasi tahap discovery selanjutnya.
* **Bahasa Objektif vs Pernyataan Mutlak:**
  * *Hindari kata mutlak tanpa bukti:* "Semua proses manual sangat lambat dan tidak efisien."
  * *Gunakan formulasi empiris terukur:* "Proses persetujuan melibatkan beberapa perpindahan dokumen fisik tanpa penomoran resmi, menyulitkan pelacakan status permohonan dan membutuhkan waktu 3-5 hari kerja."

### 2. Definisi & Klasifikasi Stakeholder
* **Definisi:** Pihak yang memengaruhi atau dipengaruhi oleh keberadaan dan hasil suatu sistem.
* **Klasifikasi:**
  * **Stakeholder Primer:** Pengguna inti yang berinteraksi langsung dengan sistem atau sangat bergantung pada operasional harian sistem (misal: mahasiswa pemohon, petugas loket, verifikator).
  * **Stakeholder Sekunder:** Pihak pendukung yang memengaruhi sistem secara tidak langsung melalui kepatuhan regulasi, penyediaan akses data, atau penyediaan infrastruktur TI (misal: pimpinan unit, tim keamanan siber, auditor internal).
* **Matriks Pemetaan Kepentingan Stakeholder:**
  Menganalisis 4 dimensi kunci:
  1. *Tingkat Kepentingan (*Interest*)* terhadap perubahan sistem.
  2. *Tingkat Pengaruh (*Power/Influence*)* terhadap keputusan proyek.
  3. *Tingkat Penguasaan Informasi/Keahlian Proses Bisnis.*
  4. *Preferensi Komunikasi & Strategi Pendekatan Elisitasi.*

### 3. Ruang Lingkup Proyek (*Project Scope*) & Scope Canvas
* **Urgensi Scope:** Menetapkan batas tanggung jawab tim proyek dan mencegah perluasan lingkup tanpa kendali (*Scope Creep*).
* **Scope Canvas:**
  * **In-Scope (Fokus Pekerjaan):** Fungsi spesifik, unit kerja, dan alur layanan yang disepakati untuk diselesaikan.
  * **Out-of-Scope (Dikecualikan):** Batasan eksplisit hal-hal yang TIDAK dikerjakan dalam periode ini (misal: "Proyek berhenti pada analisis dan rancangan desain logis; tidak mencakup pengadaan server dan koding sistem penuh").
* **Prinsip Akademis:** Lebih baik menganalisis satu alur layanan secara tuntas, valid, dan mendalam daripada menganalisis seluruh ekosistem organisasi secara dangkal.

### 4. Analisis Kelayakan Awal (*Feasibility Study*)
*Evaluasi berbasis asumsi logis yang realistis dan transparan, bukan sekadar angka persentase semu:*
* **Kelayakan Operasional:** Menilai kesiapan organisasi mengadopsi sistem baru, dampak terhadap beban kerja, dan kesediaan adaptasi pengguna.
* **Kelayakan Teknis:** Menilai ketersediaan perangkat keras/lunak, integrasi dengan infrastruktur warisan (*legacy*), dan kapabilitas teknis tim.
* **Kelayakan Ekonomi:** Estimasi biaya-manfaat (*cost-benefit*) secara konseptual dan rasional.
* **Kelayakan Jadwal:** Keselarasan target analisis dan perancangan terhadap durasi kalender akademik semester berjalan.
* **Isu Kritis: Akses Stakeholder:** Ketersediaan izin wawancara, observasi lapangan, dan akses terhadap bukti dokumen organisasi.

### 5. Batasan Proyek (*Constraints*)
* **Definisi:** Pagar pembatas yang membatasi ruang solusi dan proses pengembangan. Berbeda dari *requirement* (yang menentukan fungsi sistem), *constraint* membatasi pilihan arsitektur, teknologi, atau hukum yang boleh digunakan.
* **Tipologi Constraint:**
  * *Regulasi & Privasi:* Kepatuhan hukum perlindungan data pribadi dan SOP internal.
  * *Teknologi Warisan:* Keharusan terhubung dengan database lama tanpa mengubah skema pusat.
  * *Jadwal & Sumber Daya:* Tenggat waktu tetap dan keterbatasan lisensi alat pengembangan.

### 6. Manajemen Risiko Proyek Awal & Risk Register
* **Komponen Risiko:** Peristiwa tak terduga, Akar penyebab, Penilaian probabilitas (kemungkinan muncul), dan Penilaian dampak kualitatif.
* **Matriks Probabilitas-Dampak:** Alat navigasi untuk menentukan prioritas mitigasi risiko dari level rendah hingga kritis.
* **Risk Register Khusus Proyek Mahasiswa:**
  | Risiko Spesifik | Kategori | Strategi Respons / Mitigasi |
  | :--- | :--- | :--- |
  | Stakeholder sulit ditemui / sibuk | Akses | Jadwalkan jauh hari; gunakan surat pengantar resmi dosen; siapkan instrumen ringkas. |
  | Data operasional tidak boleh diakses | Privasi | Ajukan prosedur anonimisasi; gunakan data dummy realistis berbasis struktur asli. |
  | *Scope Creep* (lingkup melebar liar) | Lingkup | Tegakkan batas *Out-of-Scope* pada charter; tolak penambahan fitur tanpa penyesuaian jadwal. |
  | Temuan antar-narasumber saling bertentangan | Analisis | Lakukan triangulasi silang data; konfirmasi langsung melalui observasi alur nyata. |

### 7. Esensi Dinamis Project Charter & 7 Langkah Penyusunan
* **Karakteristik Dokumen:** Dokumen pengarah awal (*living baseline*) yang dinamis dan fleksibel. Wajib direvisi apabila pada tahap discovery ditemukan bukti lapangan baru yang membantah asumsi awal.
* **Alur 7 Langkah Praktis Penyusunan (CPMK-01):**
  $$\text{1. Pemilihan Konteks} \to \text{2. Problem Statement} \to \text{3. Pemetaan Stakeholder} \to \text{4. Ruang Lingkup} \to \text{5. Analisis Kelayakan} \to \text{6. Risk Register} \to \text{7. Pemeriksaan Konsistensi}$$

---

# PERTEMUAN 03: TEKNIK ELICITATION, ETIKA, CONSENT, DAN TRIANGULASI BUKTI

### 1. Hakikat Elisitasi: Menggali Bukti vs Menanyakan Fitur
* **Definisi Elisitasi:** Proses proaktif untuk memperoleh, mengekstrak, dan memahami kebutuhan, kendala kerja, regulasi operasional, serta konteks riil stakeholder.
* **Kelemahan Pertanyaan *"Fitur apa yang Anda inginkan?"*:** Stakeholder cenderung mengutarakan solusi prematur, meniru fitur aplikasi populer, atau menyampaikan kebiasaan subjektif yang belum tentu menjawab akar masalah.
* **Alur Penyelidikan Analis:**
  $$\text{Pernyataan Stakeholder (*Statements*)} \longrightarrow \text{Bukti Nyata (*Evidence*)} \longrightarrow \text{Pola Berulang (*Patterns*)} \longrightarrow \text{Kebutuhan Sistem (*Needs*)}$$

### 2. Pemilihan Teknik Elisitasi Berdasarkan Karakteristik Kebutuhan
| Pertanyaan Pemilihan Teknik | Teknik Elisitasi | Karakteristik Utama & Sasaran |
| :--- | :--- | :--- |
| Butuh penjelasan mendalam dan klarifikasi detail kontekstual? | **Wawancara (*Interview*)** | Tatap muka personal, fleksibel, mendalam, kualitatif. |
| Perlu melihat pekerjaan aktual dan memverifikasi klaim narasumber? | **Observasi (*Observation*)** | Mengamati alur nyata di lapangan, membongkar disparitas antara teori dan praktik. |
| Responden tersebar banyak dan butuh pola kecenderungan umum? | **Survei (*Questionnaire*)** | Jangkauan luas, kuantitatif, membutuhkan instrumen pertanyaan yang sangat jelas. |
| Perlu menyamakan pemahaman dan resolusi perbedaan kepentingan? | **Lokakarya (*Workshop/JAD*)** | Interaksi intensif antar-stakeholder, diskusi terarah, menghasilkan konsensus. |
| Perlu bukti aturan formal, format arsip, dan alur legal? | **Analisis Dokumen (*Document Analysis*)** | Mengkaji formulir fisik, laporan, SOP resmi, dan template kerja. |

### 3. Merancang Pedoman Wawancara (*Interview Guide*)
* **Struktur Dokumen Pedoman:**
  * **Objective:** Sasaran spesifik informasi yang ingin dicapai.
  * **Core Questions:** Pertanyaan seputar alur kerja normal, tantangan, pengecualian, dan pengambilan keputusan.
  * **Probe / Follow-up:** Pertanyaan eksplorasi lanjutan untuk membedah istilah khusus atau klaim narasumber.
  * **Evidence Sought:** Bukti fisik/arsip yang ingin diverifikasi langsung saat sesi berlangsung.
* **Aturan Pertanyaan:** Gunakan pertanyaan terbuka (*open-ended*). Dilarang menggunakan pertanyaan memimpin (*leading question*), seperti: *"Bukankah pembuatan website baru akan menyelesaikan masalah antrean Anda?"*.

### 4. Perbandingan Mendalam: Workshop vs Survei
| Parameter | Lokakarya (*Workshop*) | Survei (*Survey*) |
| :--- | :--- | :--- |
| **Kedalaman Informasi (*Depth*)** | Tinggi; mengklarifikasi perbedaan istilah dan logika alur secara langsung. | Menengah-Rendah; menangkap pola umum tanpa pendalaman instan. |
| **Jangkauan Responden (*Reach*)** | Terbatas pada perwakilan kunci (5-15 orang). | Sangat luas (puluhan hingga ribuan responden). |
| **Tingkat Interaksi** | Sangat interaktif; memicu debat dan kesepakatan langsung. | Satu arah; bergantung total pada pemahaman mandiri responden. |
| **Persiapan Analis** | Fasilitasi ruangan, penetapan agenda, dan manajemen konflik. | Desain butir instrumen bebas bias dan pengujian validitas instrumen. |

### 5. Etika Penelitian dan Persetujuan (*Consent*)
*Consent bukan sekadar tanda tangan administratif, melainkan perlindungan hak stakeholder:*
* **Purpose:** Menjelaskan secara transparan tujuan pengumpulan data dan batasan pemanfaatannya.
* **Consent:** Stakeholder sadar dan menyetujui aktivitas perekaman, pemotretan, atau pencatatan yang dilakukan.
* **Minimal Data:** Membatasi data yang dikumpulkan hanya pada kebutuhan perancangan sistem; jangan meminta data rahasia pribadi tanpa urgensi.
* **Permission:** Memastikan ada izin resmi pimpinan sebelum mengambil arsip internal organisasi.
* **Confidentiality:** Menjelaskan batas kerahasiaan identitas dan perlindungan data dalam laporan akademik.

### 6. Prinsip Triangulasi Bukti (*Evidence Triangulation*)
* **Konsep:** Membandingkan informasi dari minimal 2 hingga 3 sumber atau teknik berbeda (misal: Hasil Wawancara $\leftrightarrow$ Observasi Alur Nyata $\leftrightarrow$ Bukti Dokumen Formulir).
* **Menyikapi Pertentangan Bukti:**
  * *Kasus:* Wawancara menyatakan permohonan selesai 1 hari, tetapi observasi menemukan dokumen menumpuk 3 hari di meja verifikator.
  * *Sikap Analis:* Perbedaan bukti bukan untuk mencari siapa yang salah, melainkan fakta bahwa proses nyata memiliki hambatan informal. Status temuan ditandai "Belum Terkonfirmasi" hingga bukti tambahan diklarifikasi.

### 7. Struktur Instrumen Elisitasi & Tata Kelola Peer-Feedback
* **Struktur Instrumen Standar:**
  $$\text{Objective} \longrightarrow \text{Target Stakeholder} \longrightarrow \text{Daftar Pertanyaan/Indikator} \longrightarrow \text{Target Bukti Faktual} \longrightarrow \text{Rencana Etika \& Consent}$$
* **Siklus Peer Review:** Pemeriksaan oleh rekan sejawat untuk mendeteksi pertanyaan redundan, istilah ambigu, atau potensi pelanggaran etika $\to$ Revisi instrumen $\to$ Penyimpanan jejak versi di repositori Git.

---

# PERTEMUAN 04: SINTESIS TEMUAN ANALISIS

### 1. Pipeline Sintesis Temuan
$$\text{Bukti Mentah} \longrightarrow \text{Klaster Affinity} \longrightarrow \text{Akar Masalah (RCA)} \longrightarrow \text{Proses As-Is} \longrightarrow \text{Pain Point Terlacak} \longrightarrow \text{Opportunity Statement}$$

### 2. Metode Affinity Mapping (Diagram Afinitas)
* **Definisi:** Metode pengelompokan temuan discovery berbasis kedekatan tema secara induktif (*bottom-up*), tanpa memaksakan kategori prasangka di awal.
* **Aturan Catatan Temuan:** Wajib berupa catatan spesifik berbasis data empiris, bukan generalisasi abstrak (contoh: gunakan *"Pemohon tidak mengetahui dokumennya berada di meja siapa"*, bukan *"Komunikasi buruk"*).
* **Validasi Tema:** Setiap label kelompok tema wajib didukung oleh minimal dua bukti faktual independen.

### 3. Analisis Akar Masalah (*Root Cause Analysis - RCA*)
* **Gejala (*Symptom*):** Kondisi kasat mata yang muncul di permukaan lingkungan operasional (contoh: antrean panjang pemohon di loket).
* **Akar Masalah (*Root Cause*):** Kerentanan mendasar pada alur proses, tata kelola data, atau mekanisme kontrol yang memicu gejala berulang (contoh: pencatatan dokumen dilakukan pada spreadsheet offline personal tanpa integrasi jaringan).

### 4. Pemodelan Kondisi Aktual (*As-Is Process*)
* **Potret Realitas Faktual:** Menggambarkan bagaimana aktivitas bisnis benar-benar berlangsung di lapangan saat ini.
* **Bukan Salinan SOP Ideal:** Diagram As-Is wajib menampilkan penundaan waktu, pekerjaan manual yang berulang, verifikasi tidak resmi, dan hambatan komunikasi.
* **Pusat Variasi:** Wajib memperlihatkan siapa aktor pelaksana, dokumen fisik yang berpindah, dan titik pengambilan keputusan.

### 5. Karakteristik Pain Point Terlacak (*Traceable Pain Points*)
*Setiap Pain Point yang sah wajib memiliki 4 atribut:*
1. **ID Unik:** Kodefikasi resmi sistematis (misal: `PP-01`, `PP-02`).
2. **Lokasi Titik Proses:** Menunjuk secara presisi pada langkah aktivitas tertentu di dalam diagram As-Is.
3. **Bukti Faktual (*Evidence*):** Mengacu pada kutipan transkrip wawancara (`W-xx`) atau catatan observasi (`O-xx`).
4. **Dampak Terukur (*Measurable Impact*):** Waktu tunggu terbuang, kesalahan transkripsi data, atau beban kerja lembur.
* *Larangan Analis:* Dilarang menulis pain point yang menyiratkan solusi, seperti *"Pain Point: Belum ada aplikasi Android"* (itu adalah ketiadaan produk, bukan masalah proses bisnis).

### 6. Perumusan Peluang Perbaikan (*Opportunity Statement*)
* **Prinsip Utama:** Berorientasi pada HASIL BISNIS (*outcome-based*), bukan MENGUNCI BENTUK TEKNOLOGI (*solution-locking*).
* **Perbandingan Formulasi:**
  * *Salah (Mengunci Solusi):* "Membangun sistem notifikasi WhatsApp otomatis."
  * *Benar (Berorientasi Hasil):* "Meningkatkan transparansi status permohonan agar pemohon dapat memantau progres secara mandiri tanpa membebani staf loket."

### 7. As-Is Walkthrough & Kelengkapan Milestone 1
* **As-Is Walkthrough:** Meninjau model proses bersama stakeholder operasional untuk menemukan *defect* (aktor yang terlewat, alur keputusan tersembunyi, atau asumsi yang keliru).
* **Paket Deliverable Milestone 1 (Discovery & Charter):**
  * Dokumen Project Charter yang diselaraskan dengan bukti lapangan.
  * Diagram Affinity Mapping.
  * Pohon Masalah / Diagram RCA.
  * Model Alur Proses As-Is.
  * Daftar Pain Point terlacak lengkap dengan ID dan bukti.
  * Rumusan Opportunity Statement terpadu.

---

# PERTEMUAN 05: REQUIREMENTS ENGINEERING

### 1. Esensi Rekayasa Kebutuhan (*Requirements Engineering*)
* **Peran Utama Analis:** Mengubah bahasa keluhan dan permasalahan stakeholder menjadi bahasa spesifikasi teknis yang jelas, terstruktur, dapat diuji (*testable*), diprioritaskan, dan dapat dilacak (*traceable*).
* **Alur Transformasi 4 Tahap:**
  $$\text{Bukti Discovery} \xrightarrow{\text{Pemisahan Fakta}} \text{Kebutuhan Sistem} \xrightarrow{\text{Spesifikasi Eksplisit}} \text{FR / NFR} \xrightarrow{\text{Uji Kondisi}} \text{Acceptance Criteria} \xrightarrow{\text{Rantai Dua Arah}} \text{RTM}$$

### 2. Kebutuhan Fungsional (*Functional Requirements - FR*)
* **Definisi:** Pernyataan eksplisit mengenai perilaku, layanan, dan komputasi yang wajib dijalankan oleh sistem perangkat lunak.
* **Rumus Berpikir Formulasi FR Berkualitas:**
  $$\mathbf{FR} = [\text{Kondisi / Pemicu}] + [\text{Aktor yang Relevan}] + [\text{Respons / Perilaku Sistem}] + [\text{Hasil yang Dapat Diverifikasi}]$$
* **Contoh:**
  * *Lemah (Ambigu):* "Sistem harus memiliki menu persetujuan yang baik."
  * *Kuat (Dapat Diuji):* "`FR-03`: Ketika staf verifikator membuka permohonan berkas lengkap, sistem harus menyediakan fungsi untuk menetapkan status 'Disetujui' atau 'Ditolak' disertai pencatatan identitas verifikator dan stempel waktu (*timestamp*)."

### 3. Kebutuhan Non-Fungsional (*Non-Functional Requirements - NFR*)
* **Definisi:** Atribut kualitas arsitektur, batasan kinerja, keandalan, dan tata kelola lingkungan sistem.
* **Kategori Kualitas (ISO/IEC 25010):** *Security*, *Performance*, *Reliability*, *Availability*, *Maintainability*, *Usability*.
* **Prinsip Anti-Slop NFR:**
  * Hindari kata sifat abstrak tanpa konteks: "sistem harus cepat", "sistem harus aman".
  * Jangan mengarang angka batas tanpa data empiris/kebijakan formal.
  * Contoh yang tepat: "`NFR-SEC-01`: Data rekam medis permohonan hanya dapat diakses oleh pemilik permohonan dan petugas verifikator yang memiliki hak akses aktif berdasarkan peran (*Role-Based Access Control*)."

### 4. Aturan Bisnis (*Business Rules - BR*) vs FR
* **Business Rule (BR):** Kebijakan, peraturan formal, atau ketetapan hukum yang berlaku di organisasi terlepas dari keberadaan sistem komputer. Memiliki sumber kebijakan formal.
* **Functional Requirement (FR):** Perilaku perangkat lunak yang dirancang untuk menerapkan atau menegakkan aturan bisnis tersebut.
* **Contoh Hubungan:**
  * `BR-01`: "Keputusan persetujuan permohonan hanya sah jika disahkan oleh Kepala Bagian Tata Usaha (Sumber: SK Dekan No. 04/2024)."
  * `FR-04`: "Sistem harus memblokir opsi tombol penetapan status 'Disetujui' bagi akun pengguna di luar peran Kepala Bagian Tata Usaha."

### 5. Representasi Kebutuhan: User Story vs Use Case Narrative
* **User Story:** Ringkas, fokus pada nilai bisnis dari kacamata aktor pengguna.
  * *Format:* `"Sebagai [Peran Aktor], saya ingin [Fungsi/Kebutuhan] sehingga [Nilai Bisnis/Manfaat]."`
* **Use Case Narrative:** Terstruktur, merinci langkah demi langkah interaksi prosedural sistem, mencakup prasyarat (*precondition*), pemicu (*trigger*), alur normal (*main flow*), alur alternatif (*alternate flow*), penanganan error (*exception flow*), dan kondisi akhir (*postcondition*).

### 6. Kriteria Penerimaan (*Acceptance Criteria - AC*)
* **Fungsi:** Mendefinisikan kondisi objektif yang harus dipenuhi agar implementasi kebutuhan dapat diterima dan diverifikasi kebenarannya.
* **Format Penulisan:**
  * *Checklist Terukur:* Pernyataan kondisi biner (Ya/Tidak).
  * *Format Gherkin / BDD:*
    * **GIVEN** (Kondisi prasyarat data/sistem)
    * **WHEN** (Tindakan yang dipicu oleh aktor)
    * **THEN** (Respons terverifikasi yang diberikan oleh sistem)

### 7. Prioritas Kebutuhan Berbasis Alasan
*Prioritas ditentukan berdasarkan argumen rasional yang terdokumentasi, bukan intuisi pribadi:*
1. **Nilai bagi Stakeholder:** Kontribusi nyata terhadap penyelesaian pain point utama.
2. **Urgensi:** Risiko kerugian apabila kebutuhan ditunda pengembangannya.
3. **Risiko Teknis:** Tingkat kesulitan implementasi dan ketidakpastian solusi.
4. **Dependensi Kebutuhan:** Keberadaan kebutuhan lain yang menjadi prasyarat teknis.

### 8. Requirements Traceability Matrix (RTM)
* **Tujuan RTM:** Mencegah kebutuhan menjadi "yatim" (*orphan requirement*) tanpa asal-usul, dan mencegah lahirnya fitur liar tanpa justifikasi kebutuhan (*gold plating*).
* **Format Kolom RTM Standar:**
  | Req ID | Kategori | Sumber Bukti | Kode Pain Point | Kriteria Penerimaan | Artefak Lanjutan (Model) | Elemen Desain (SDD) | Status Baseline |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | `FR-01` | Fungsional | Wawancara `W-01` | `PP-02` | `AC-01`, `AC-02` | `UC-01`, `ACT-01` | Antarmuka Cek Status | Baseline v1.0 |
  | `BR-01` | Aturan Bisnis | SK Rektor `D-02` | `PP-01` | Validasi Otorisasi | BPMN Gateway | Modul Hak Akses RBAC | Baseline v1.0 |
  | `NFR-01`| Keamanan | Kebijakan TI `D-05`| - | Uji Enkripsi | Arsitektur Jaringan | Protokol TLS 1.3 | Baseline v1.0 |

### 9. Struktur Dokumen Draft SRS (Baseline Hidup)
Dokumen SRS memuat: 1. Konteks & Scope; 2. Karakteristik Stakeholder; 3. Daftar FR & NFR; 4. Aturan Bisnis (BR); 5. User Story / Gambaran Use Case; 6. Kriteria Penerimaan; 7. Prioritas Kebutuhan; 8. Matriks Keterlacakan Awal (RTM).  
*SRS adalah living baseline yang siap diperbarui secara terkontrol saat pemodelan proses menemukan anomali baru.*

---

# PERTEMUAN 06: PEMODELAN PROSES BISNIS BPMN 2.0.2

### 1. Esensi Standardisasi BPMN 2.0.2 (*Business Process Model and Notation*)
* **Kelemahan Narasi Tekstual:** Narasi alur kerja sering menyembunyikan perpindahan tanggung jawab (*handoff*), titik percabangan keputusan, dan penanganan kegagalan (*exception*).
* **Tujuan BPMN:** Menyediakan standar visual industri yang universal untuk merepresentasikan alur kerja lintas aktor secara transparan, dapat diuji logikanya, dan siap diaudit.

### 2. Anatomi Notasi BPMN 2.0.2
* **Events (Peristiwa):**
  * **Start Event (Lingkaran Tipis):** Pemicu dimulainya proses (contoh: Pemohon membutuhkan surat).
  * **Intermediate Event (Lingkaran Ganda):** Peristiwa di tengah alur (contoh: Timer batas waktu tunggu).
  * **End Event (Lingkaran Tebal):** Kondisi terminasi akhir yang dicapai proses.
* **Activities / Tasks (Aktivitas Pekerjaan):**
  * Kotak persegi bersudut tumpul yang menunjukkan unit pekerjaan terukur.
  * *Konvensi Penamaan:* Wajib diawali **Kata Kerja Aktif Transitif + Objek Spesifik** (contoh: *"Periksa kelengkapan berkas"*, bukan *"Proses berkas"* atau *"Klik tombol"*).
* **Gateways (Gerbang Logika):**
  * Pengendali percabangan (*diverging*) dan penggabungan (*converging*) alur proses.
  * **Exclusive Gateway / XOR (Belah Ketupat bertanda silang X atau polos):** Menetapkan pemilihan SATU jalur alternatif eksklusif berdasarkan kondisi evaluasi (contoh: Berkas Lengkap? `[Lengkap]` vs `[Tidak Lengkap]`).
  * Setiap cabang keluar dari gateway WAJIB memiliki label kondisi yang jelas.
* **Pools dan Lanes:**
  * **Pool:** Merepresentasikan entitas organisasi atau batas keseluruhan proses partisipan.
  * **Lane:** Sub-partisi di dalam Pool yang menunjukkan peran fungsional (*role*), jabatan, atau sistem tertentu yang bertanggung jawab mengeksekusi aktivitas.
  * *Defect Tanggung Jawab:* Menempatkan tugas verifikasi di lane pemohon adalah kesalahan fatal dalam pemodelan tata kelola.
* **Boundary Events & Exception Handling:**
  * Event yang ditempelkan langsung pada batas luar aktivitas (*task boundary*).
  * Menangani kondisi kegagalan atau pembatalan di luar jalur utama (contoh: *Timer Boundary Event* 3 hari untuk perbaikan berkas; jika batas waktu habis, alur bergerak ke pembatalan permohonan).

### 3. Komparasi Proses Bisnis: As-Is vs To-Be
| Parameter | Diagram As-Is (Proses Faktual) | Diagram To-Be (Proses Usulan) |
| :--- | :--- | :--- |
| **Sumber Kebenaran** | Fakta empiris temuan discovery di lapangan. | Penyelarasan kebutuhan SRS dan resolusi pain point. |
| **Representasi Masalah**| Memotret friksi, tumpukan berkas, catatan lokal offline. | Menggambarkan integrasi alur baru yang terkoordinasi. |
| **Keterlacakan Pain Point**| Kode `PP-xx` ditempelkan langsung pada titik aktivitas bermasalah. | Setiap perubahan alur kerja wajib merujuk pada `PP-xx` yang diselesaikan. |
| **Otomatisasi** | Tanpa otomatisasi asumtif. | Otomatisasi hanya diterapkan jika didukung oleh FR yang valid. |

### 4. Menjaga Traceability pada Pemodelan To-Be
$$\text{Pain Point (PP-02: Status Tidak Terlihat)} \longrightarrow \text{Kebutuhan (FR-01: Menampilkan Status)} \longrightarrow \text{Aktivitas To-Be (Task 'Lihat Status')}$$
*Audit Dua Arah: Setiap perubahan pada proses To-Be harus memiliki alasan kebutuhan yang sah; dan setiap kebutuhan fungsional kritis harus terwujud di dalam alur proses.*

### 5. Design Critique & Deteksi 6 Kategori Defect BPMN
1. **Defect Notasi:** Penggunaan simbol yang menyalahi semantik standar BPMN 2.0.2.
2. **Defect Logika:** Alur terputus, loop tanpa akhir (*infinite loop*), alur tanpa pintu keluar (*dead end*).
3. **Defect Gateway:** Gateway percabangan tanpa kondisi evaluasi yang jelas, atau kondisi saling tumpang tindih.
4. **Defect Exception:** Hanya memodelkan skenario ideal (*happy path*) dan mengabaikan penolakan atau pembatalan.
5. **Defect Lane:** Aktivitas dikerjakan oleh peran yang tidak berwenang (salah alokasi lane).
6. **Defect Traceability:** Memasukkan tugas sistem baru yang tidak memiliki dasar referensi di dalam SRS.

### 6. Sinkronisasi Dua Arah: BPMN $\longleftrightarrow$ SRS
Pemodelan BPMN berfungsi sebagai alat uji ketajaman kebutuhan. Ketika dalam perancangan diagram ditemukan cabang proses baru (misal: penanganan dokumen kedaluwarsa), analis wajib memperbarui dokumen SRS (menambahkan FR baru, BR baru, dan mengupdate RTM).

---

# PERTEMUAN 07: USE CASE, ACTIVITY DIAGRAM, DAN PEMBEKUAN SRS BASELINE

### 1. Fondasi Pemodelan Perilaku Sistem (*Behavioral Modeling*)
* **Jembatan Konseptual:** Mengubah pernyataan kebutuhan tekstual dari SRS menjadi model perilaku sistem yang dinamis, konsisten, dan siap diimplementasikan.
* **3 Fondasi Utama Pemodelan Perilaku:**
  1. **System Boundary (Batasan Sistem):** Kotak pembatas yang memisahkan tanggung jawab komputasi internal perangkat lunak dari entitas luar.
  2. **Aktor (*Actor*):** Peran eksternal (manusia, departemen, atau perangkat lunak eksternal) yang berinteraksi dengan sistem untuk mencapai tujuan tertentu. Aktor adalah representasi peran (*role*), bukan nama personal.
  3. **Use Case:** Representasi tujuan bermakna (*meaningful goal*) yang ingin dicapai oleh aktor melalui interaksi terencana dengan sistem. Penamaan menggunakan **Kata Kerja + Objek** (contoh: *"Ajukan Peminjaman"*, *"Periksa Berkas"*).

### 2. Notasi dan Anatomi Use Case Diagram
* **Aktor:** Digambarkan dengan simbol stick figure (pengguna manusia) atau kotak bertuliskan `<<system>>` (sistem luar).
* **Use Case:** Digambarkan dengan elips horizontal di dalam kotak *System Boundary*.
* **Relasi Asosiasi:** Garis lurus solid antara Aktor dan Use Case yang menunjukkan keterlibatan langsung.
* **Relasi Antar-Use Case:**
  * **Relasi `<<include>>`:** Relasi ketergantungan wajib di mana use case dasar SELALU memanggil use case yang di-include untuk menyelesaikan operasinya (contoh: *"Ajukan Permohonan"* `<<include>>` *"Validasi Format Berkas"*).
  * **Relasi `<<extend>>`:** Relasi perluasan kondisional di mana use case ekstensi HANYA dieksekusi jika kondisi prasyarat tertentu terpenuhi pada titik perluasan (*extension point*) (contoh: *"Pendaftaran Pasien"* `<<extend>>` *"Verifikasi Kepesertaan BPJS"* jika pasien memilih pembayaran asuransi).

### 3. Struktur Anatomi Use Case Narrative
*Spesifikasi narasi teks yang mendampingi diagram use case:*
1. **Identitas Use Case:** ID Unik (`UC-xx`), Nama Use Case, Aktor Utama, Aktor Pendukung.
2. **Deskripsi Singkat:** Penjelasan ringkas nilai fungsional yang dicapai.
3. **Prasyarat (*Precondition*):** Kondisi yang WAJIB bernilai benar sebelum interaksi dimulai (misal: "Pengguna telah berhasil login").
4. **Pemicu (*Trigger*):** Aksi awal yang menginisiasi proses.
5. **Alur Utama (*Main Flow / Happy Path*):** Urutan interaksi normal bernomor langkah ketika seluruh skenario berhasil tanpa hambatan.
6. **Alur Alternatif (*Alternate Flow*):** Variasi alur kerja yang valid di mana tujuan akhir use case tetap berhasil dicapai melalui jalan berbeda.
7. **Alur Pengecualian (*Exception Flow*):** Skenario penanganan kegagalan ketika aturan dilanggar, koneksi luar terputus, atau sistem membatalkan proses.
8. **Kondisi Akhir (*Postcondition*):** Keadaan data dan sistem yang dijamin terwujud setelah use case selesai.

### 4. Pemodelan Dinamis: Activity Diagram (UML)
* **Definisi:** Diagram perilaku UML yang memodelkan aliran kontrol sekuensial, percabangan logika, iterasi, dan aktivitas paralel di dalam suatu proses sistem.
* **Elemen Notasi Dasar Activity Diagram:**
  * **Initial Node:** Lingkaran hitam padat penanda titik mula aliran kontrol.
  * **Activity / Action State:** Kotak persegi bersudut tumpul (*rounded rectangle*) yang menunjukkan tindakan terukur.
  * **Control Flow:** Garis panah berarah yang menunjukkan transisi aktivitas.
  * **Decision Node:** Belah ketupat untuk mencabangkan satu input menjadi beberapa alternatif berdasar *guard condition* (`[kondisi]`).
  * **Merge Node:** Belah ketupat untuk menyatukan kembali cabang-cabang alternatif menjadi satu aliran tunggal.
  * **Fork Node:** Garis batang tebal hitam mendatar/tegak untuk memecah satu aliran kontrol menjadi DUA ATAU LEBIH aktivitas paralel independen.
  * **Join Node:** Garis batang tebal hitam untuk menyinkronkan kembali aktivitas paralel (semua aktivitas paralel harus selesai sebelum aliran lanjut).
  * **Activity Final Node:** Lingkaran padat hitam di dalam cincin lingkaran (lingkaran banteng) penanda proses selesai.
  * **Swimlanes (Kolom Partisi):** Pembagi visual vertikal atau horizontal untuk memperjelas tanggung jawab siapa yang mengeksekusi aktivitas (Aktor A, Sistem, Aktor B).

### 5. Komparasi Komprehensif: Use Case vs Flowchart vs Activity Diagram
| Parameter Evaluasi | Use Case Diagram | Flowchart Tradisional | Activity Diagram (UML) |
| :--- | :--- | :--- | :--- |
| **Tujuan Utama** | Memetakan interaksi batas sistem antara aktor luar dan kapabilitas sistem (**APA** yang dilakukan sistem). | Menggambarkan urutan langkah logis prosedural dari algoritma atau program teknis. | Menggambarkan alur aktivitas koordinasi proses bisnis atau logika internal sistem (**BAGAIMANA** proses mengalir). |
| **Fokus Pemodelan** | Fungsionalitas dari sudut pandang pemakai eksternal. | Logika kontrol program tingkat rendah. | Alur aktivitas operasional, penanganan kondisi, dan sinkronisasi paralel. |
| **Simbol Kunci** | Aktor (Stick figure), Use Case (Elips), Batas Sistem (Kotak). | Oval (Start/End), Persegi (Proses), Belah Ketupat (Decision). | Initial/Final Node, Action (Rounded box), Decision/Merge, Fork/Join, Swimlanes. |
| **Penonjolan Aktor** | **Sangat Dominan** (aktor berada di luar batas sistem). | **Tidak Ada** (fokus internal proses). | **Eksplisit** melalui pemisahan kolom partisi (*Swimlanes*). |
| **Logika Alur Rinci** | Tidak memodelkan urutan langkah sekuensial. | Memodelkan langkah demi langkah secara linear. | Memodelkan urutan alur secara dinamis lengkap dengan guard condition. |
| **Proses Paralel (Konkurensi)**| **Tidak Mendukung** | **Umumnya Tidak Mendukung** (alur sekuensial tunggal). | **Mendukung Penuh** melalui notasi sinkronisasi Fork dan Join Node. |
| **Waktu Penggunaan** | Tahap analisis kebutuhan awal untuk mengunci ruang lingkup. | Tahap perancangan algoritma teknis dan kalkulasi modular. | Tahap analisis proses bisnis kompleks dan penjabaran skenario Use Case. |
| **Tingkat Abstraksi** | Sangat Tinggi (Konseptual). | Rendah hingga Menengah (Teknis/Prosedural). | Menengah (Jembatan antara Analisis Kebutuhan dan Desain Solusi). |

### 6. Rantai Keterlacakan Penuh (*Full-Traceability Chain*)
$$\text{Bukti Discovery (W/O/D)} \longleftrightarrow \text{Pain Point (PP-xx)} \longleftrightarrow \text{Req ID (FR/NFR/BR)} \longleftrightarrow \text{Use Case (UC-xx)} \longleftrightarrow \text{Activity (ACT-xx)} \longleftrightarrow \text{Acceptance Criteria (AC-xx)}$$

### 7. Checklist Deteksi Defect Sebelum Pembekuan Baseline SRS
1. Aktor dinamai berdasarkan nama individu, bukan peran fungsional (*role*).
2. Use case terlalu granular pada tingkat aksi antarmuka (misal: "Klik tombol simpan").
3. Batasan sistem (*System Boundary*) tidak digambar atau batas tanggung jawabnya kabur.
4. Main flow narasi use case tidak memiliki respon balik yang diverifikasi dari sistem.
5. Skenario *alternate* atau *exception* tidak memiliki kondisi pemicu (*guard condition*).
6. Terdapat alur buntu (*dead end*) atau loop tanpa pintu terminasi pada Activity Diagram.
7. Terdapat requirement di SRS yang berstatus "yatim" (tidak memiliki representasi Use Case).
8. Inkonsistensi penamaan istilah antara narasi dokumen dan simbol diagram visual.
9. Kriteria penerimaan (*Acceptance Criteria*) bertentangan dengan alur skenario operasional.
10. Revisi artefak belum dicatat di dalam log riwayat perubahan (*change log*).

### 8. Milestone 2: Pembekuan SRS Baseline Versi 1.0
* **Makna Baseline:** Titik beku resmi (*frozen baseline*) di mana dokumen spesifikasi kebutuhan telah divalidasi dan disepakati bersama oleh tim dan dosen/klien sebagai acuan resmi perancangan arsitektur sistem (SDD).
* **Kontrol Perubahan (*Change Control*):** Setelah status baseline terkunci, tidak boleh ada penambahan atau pengubahan kebutuhan secara liar. Setiap modifikasi harus diajukan melalui mekanisme pencatatan revisi resmi di repositori.
* **Paket Deliverable:** Dokumen SRS v1.0, Diagram Use Case & Narasi Skenario, Activity Diagram UML, Matriks RTM Terpadu, Berita Acara Peer Review, dan Catatan Tindakan Perbaikan (*Corrective Actions*).

---

# MATRIKS INTEGRASI ALUR ARTEFAK & PENILAIAN AKADEMIK

### 1. Peta Jalan Evolusi Artefak (PBL IF21307)
```
[FASE DISCOVERY & INISIASI] (Pertemuan 1 - 4)
  1. Problem Framing & Kebutuhan Nyata (P1 - P2)
  2. Project Charter & Analisis Awal (P2)
  3. Instrumen Elisitasi, Etika & Triangulasi Bukti (P3)
  4. Affinity Mapping, Root Cause Analysis & Alur As-Is (P4)
  5. Perumusan Pain Points (PP-xx) & Opportunity Statement (P4)
                                |
                                v
               [MILESTONE 1: DISCOVERY & PROJECT CHARTER]
                                |
[FASE REKAYASA KEBUTUHAN & PEMODELAN PERILAKU] (Pertemuan 5 - 7)
  1. Formulasi FR, NFR, Business Rules & Acceptance Criteria (P5)
  2. Requirements Traceability Matrix / RTM Awal (P5)
  3. Pemodelan Proses Bisnis BPMN 2.0.2 As-Is vs To-Be (P6)
  4. Pemodelan Perilaku Sistem: Use Case Diagram & Narasi (P7)
  5. Pemodelan Dinamis: Activity Diagram UML dengan Swimlane (P7)
  6. Defect Hunt & Sinkronisasi Artefak (P7)
                                |
                                v
               [MILESTONE 2: FROZEN SRS BASELINE v1.0]
                                |
[EVALUASI PERTENGAHAN SEMESTER] (Pertemuan 8)
  -> Ujian Tengah Semester (UTS Individual): Validasi Komprehensif P1 - P7
```

### 2. Standar Skala Rubrik Evaluasi Akademik (Skor 1 - 4)
* **Skor 4 (79 – 100) — SANGAT BAIK:**
  Fondasi analisis akurat; ruang lingkup komprehensif; instrumen elisitasi etis dan tervalidasi triangulasi; rantai traceability utuh tanpa ada kebutuhan yatim; pemodelan BPMN, Use Case, dan Activity Diagram konsisten, terbebas dari defect logika/notasi; baseline siap dibekukan.
* **Skor 3 (65 – 79) — BAIK:**
  Konsep utama tepat; sebagian besar pain point dan akar masalah teridentifikasi berbasis bukti; terdapat kekurangan minor non-substansi pada notasi atau format skenario.
* **Skor 2 (49 – 65) — CUKUP:**
  Sebagian aspek terpenuhi, namun dokumentasi elisitasi terbatas, terdapat inkonsistensi penamaan istilah antar-artefak, atau traceability belum menghubungkan seluruh kebutuhan ke model.
* **Skor 1 (0 – 49) — KURANG:**
  Analisis tidak berbasis bukti faktual; elisitasi menyalahi etika/tanpa izin; pemodelan menyembunyikan exception (hanya happy path); ketiadaan traceability dan ketidaklengkapan komponen utama charter/SRS.

---
*Dokumen ini disusun sebagai ringkasan materi akademik utuh dan presisi untuk mata kuliah Analisis dan Desain Sistem (IF21307), Universitas Jenderal Soedirman.*
