**SOFTWARE REQUIREMENTS  
SPECIFICATION (SRS)**

**Sistem Permohonan Surat Akademik**

Contoh Draft SRS untuk IF21307 - Analisis dan Desain Sistem

| **Status Dokumen** | Draft untuk pembelajaran                                       |
|--------------------|----------------------------------------------------------------|
| **Versi**          | 0.1                                                            |
| **Tanggal**        | 15 September 2026                                              |
| **Kasus**          | Hipotetik - layanan permohonan surat akademik                  |
| **Catatan**        | Bukan spesifikasi sistem nyata dan bukan ketentuan proyek baru |

> **Dokumen ini mencontohkan struktur draft SRS pada tahap Pertemuan 5: konteks/scope, stakeholder, FR/NFR, business rules, user story/use case narrative, acceptance criteria, prioritas, dan RTM awal. Model proses/perilaku dilengkapi pada Pertemuan 6-7.**

# Daftar Isi

> 1\. Pendahuluan
>
> 2\. Deskripsi Umum Sistem
>
> 3\. Kebutuhan Fungsional
>
> 4\. Kebutuhan Non-Fungsional
>
> 5\. Business Rules
>
> 6\. User Story dan Use Case Narrative
>
> 7\. Acceptance Criteria
>
> 8\. Prioritas Kebutuhan
>
> 9\. Requirement Traceability Matrix (RTM)
>
> 10\. Baseline, Asumsi, dan Revision Notes
>
> Lampiran A. Bukti Discovery Hipotetik

# 1. Pendahuluan

## 1.1 Tujuan Dokumen

Dokumen ini memberikan contoh Software Requirements Specification (SRS) untuk Sistem Permohonan Surat Akademik. Tujuannya menunjukkan bagaimana hasil discovery diterjemahkan menjadi kebutuhan yang terstruktur, dapat diuji, diprioritaskan, dan dapat ditelusuri. Contoh ini bersifat hipotetik dan digunakan untuk pembelajaran.

## 1.2 Latar Belakang Kasus

Pada proses hipotetik saat ini, mahasiswa menyerahkan permohonan surat akademik, petugas memeriksa kelengkapan dan mencatat status pada spreadsheet lokal, kemudian verifikator mengambil keputusan. Bukti discovery menunjukkan mahasiswa sering menanyakan status karena tidak memiliki titik informasi yang dapat diakses untuk melihat progres permohonan.

## 1.3 Tujuan Sistem

- Menyediakan alur digital untuk pengajuan dan pemantauan permohonan surat akademik.

- Membantu petugas dan verifikator memperbarui status permohonan secara konsisten.

- Meningkatkan keterlacakan status bagi pemohon tanpa langsung mengunci pilihan teknologi tertentu.

## 1.4 Scope

- In scope: pengajuan permohonan, pemeriksaan data permohonan, pembaruan status, keputusan verifikasi, dan pemantauan status oleh pemohon.

- Out of scope pada draft ini: desain arsitektur teknis rinci, implementasi kode, integrasi vendor tertentu, dan metrik performa numerik yang belum divalidasi.

## 1.5 Definisi dan Singkatan

| **Istilah**     | **Definisi**                                             |
|-----------------|----------------------------------------------------------|
| **SRS**         | Software Requirements Specification.                     |
| **FR**          | Functional Requirement.                                  |
| **NFR**         | Non-Functional Requirement.                              |
| **BR**          | Business Rule.                                           |
| **AC**          | Acceptance Criteria.                                     |
| **RTM**         | Requirement Traceability Matrix.                         |
| **Pemohon**     | Mahasiswa yang mengajukan permohonan.                    |
| **Verifikator** | Peran yang meninjau dan menetapkan keputusan permohonan. |

# 2. Deskripsi Umum Sistem

## 2.1 Stakeholder dan Peran

| **Stakeholder/Peran** | **Kepentingan**                                   | **Interaksi Utama**                  |
|-----------------------|---------------------------------------------------|--------------------------------------|
| Mahasiswa/Pemohon     | Mengajukan permohonan dan mengetahui progres      | Ajukan permohonan; lihat status      |
| Petugas               | Memeriksa kelengkapan dan mengelola status proses | Validasi data; update status         |
| Verifikator           | Mengambil keputusan atas permohonan               | Setujui/tolak sesuai aturan          |
| Pengelola Layanan     | Menjaga konsistensi proses dan aturan             | Memastikan aturan layanan diterapkan |

## 2.2 System Context

![](media/image1.png)

Gambar 1. Diagram konteks konseptual Sistem Permohonan Surat Akademik.

> **Diagram ini bersifat konseptual. Detail BPMN, use case diagram, dan activity diagram merupakan artefak lanjutan yang dapat melengkapi SRS pada pertemuan berikutnya.**

## 2.3 Asumsi dan Constraint

- Pengguna memiliki identitas/akun yang dapat dikenali oleh sistem.

- Aturan kewenangan verifikator berasal dari prosedur/kebijakan layanan dan harus divalidasi pada proyek nyata.

- Ukuran kinerja numerik belum ditetapkan; kebutuhan performa dicatat sebagai kandidat yang perlu validasi jika diperlukan.

- Istilah dan ID artefak harus digunakan secara konsisten pada SRS, RTM, dan model berikutnya.

# 3. Kebutuhan Fungsional

Functional requirement menyatakan perilaku/layanan yang harus disediakan sistem. Setiap requirement diberi ID dan sumber hipotetik agar dapat ditelusuri.

| **ID**    | **Requirement Statement**                                                                                                  | **Source**                       | **Prioritas Awal** |
|-----------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------|--------------------|
| **FR-01** | Sistem harus menampilkan status terbaru permohonan kepada mahasiswa pemohon.                                               | Interview M03 / Pain Point PP-01 | High               |
| **FR-02** | Sistem harus mencatat setiap perubahan status permohonan beserta waktu perubahan dan pengguna yang melakukan perubahan.    | Observasi O02 / PP-01            | High               |
| **FR-03** | Sistem harus membatasi aksi persetujuan atau penolakan kepada pengguna dengan peran verifikator.                           | Business Rule BR-01              | High               |
| **FR-04** | Sistem harus memungkinkan mahasiswa mengajukan permohonan dengan data dan lampiran yang dipersyaratkan.                    | Opportunity OP-01                | High               |
| **FR-05** | Sistem harus memungkinkan petugas menandai permohonan sebagai memerlukan perbaikan ketika data atau lampiran belum sesuai. | Observasi O02                    | Medium             |
| **FR-06** | Sistem harus menampilkan riwayat perubahan status permohonan kepada petugas yang berwenang.                                | Kebutuhan audit proses / FR-02   | Medium             |

> **Catatan: "High/Medium" pada contoh ini adalah prioritas awal untuk tujuan pembelajaran. Pada proyek nyata, skema prioritas harus disepakati dosen/tim dan alasannya dicatat.**

# 4. Kebutuhan Non-Fungsional

NFR menyatakan kualitas atau constraint. Karena sumber kasus tidak menyediakan angka kinerja, dokumen ini tidak mengarang target numerik; hal yang membutuhkan ukuran dicatat sebagai perlu validasi.

| **ID**          | **Kategori**     | **Pernyataan**                                                                                                            | **Catatan Validasi**                               |
|-----------------|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| **NFR-SEC-01**  | Security/Privacy | Detail permohonan hanya dapat diakses oleh pemohon dan petugas yang berwenang sesuai perannya.                            | Dapat ditelusuri ke role/stakeholder dan BR-01.    |
| **NFR-AUD-01**  | Auditability     | Perubahan status harus memiliki informasi pelaku dan waktu perubahan.                                                     | Mendukung penelusuran keputusan dan terkait FR-02. |
| **NFR-CON-01**  | Consistency      | Istilah status yang ditampilkan harus konsisten dengan istilah yang digunakan pada SRS, business rules, dan model proses. | Dicek saat review lintas artefak.                  |
| **NFR-PERF-01** | Performance      | Waktu respons untuk melihat status perlu ditetapkan setelah kebutuhan stakeholder dan konteks penggunaan divalidasi.      | TBD - tidak diberi angka fiktif.                   |

# 5. Business Rules

Business rule adalah aturan yang membatasi atau mengarahkan proses dan memiliki sumber bisnis. Sistem dapat menerapkan aturan tersebut, tetapi aturan itu sendiri bukan fungsi sistem.

| **ID**    | **Rule**                                                                            | **Sumber**                         | **Related Requirement** |
|-----------|-------------------------------------------------------------------------------------|------------------------------------|-------------------------|
| **BR-01** | Hanya peran verifikator yang berwenang menetapkan keputusan Disetujui atau Ditolak. | Prosedur layanan (hipotetik)       | FR-03                   |
| **BR-02** | Permohonan yang belum lengkap tidak dapat diproses ke keputusan akhir.              | Prosedur layanan (hipotetik)       | FR-05                   |
| **BR-03** | Setiap perubahan status harus dapat ditelusuri ke pelaku dan waktu perubahan.       | Kebutuhan audit proses (hipotetik) | FR-02 / NFR-AUD-01      |

# 6. User Story dan Use Case Narrative

## 6.1 User Story

> **US-01 - Sebagai mahasiswa pemohon, saya ingin melihat status permohonan agar saya mengetahui progres tanpa harus menghubungi petugas.**

## 6.2 Use Case Narrative - UC-01 Cek Status Permohonan

| **Elemen** | **Deskripsi** |
|---|---|
| **Aktor Utama** | Mahasiswa/Pemohon |
| **Precondition** | Permohonan telah tercatat dan pengguna teridentifikasi sebagai pemohon yang sah. |
| **Trigger** | Mahasiswa membuka detail permohonan. |
| **Main Flow** | 1) Sistem mengenali identitas pemohon.<br>2) Sistem mengambil data permohonan milik pemohon.<br>3) Sistem mengambil status terbaru.<br>4) Sistem menampilkan status dan waktu pembaruan. |
| **Alternate Flow** | Jika belum ada perubahan setelah pengajuan, sistem menampilkan status awal yang tersimpan. |
| **Exception** | Jika permohonan bukan milik pengguna yang sedang masuk, akses ditolak sesuai NFR-SEC-01. |
| **Postcondition** | Tidak ada perubahan data; informasi status ditampilkan. |

# 7. Acceptance Criteria

Acceptance criteria terkait langsung dengan requirement dan digunakan untuk memeriksa apakah makna requirement telah terpenuhi.

| **Related Req** | **AC ID** | **Kriteria Penerimaan**                                                                                                                      |
|-----------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **FR-01**       | **AC-01** | Given permohonan milik mahasiswa tersimpan, when mahasiswa membuka detail permohonan, then sistem menampilkan status terbaru yang tersimpan. |
| **FR-01**       | **AC-02** | Sistem menampilkan waktu pembaruan status bersama status yang ditampilkan.                                                                   |
| **FR-02**       | **AC-03** | Setelah petugas mengubah status, riwayat perubahan menyimpan status, waktu, dan pengguna yang melakukan perubahan.                           |
| **FR-03**       | **AC-04** | Pengguna tanpa peran verifikator tidak dapat menjalankan aksi Disetujui/Ditolak.                                                             |
| **FR-04**       | **AC-05** | Permohonan yang memenuhi data wajib dapat disimpan sebagai permohonan baru dan memperoleh identitas permohonan.                              |
| **FR-05**       | **AC-06** | Petugas dapat menandai permohonan sebagai perlu perbaikan dan status tersebut terlihat pada detail permohonan.                               |

# 8. Prioritas Kebutuhan

Prioritas ditentukan dengan mempertimbangkan nilai bagi stakeholder, urgensi, risiko, dependency, dan kontribusi terhadap penyelesaian pain point. Contoh berikut menunjukkan alasan, bukan metode prioritisasi formal tertentu.

| **Requirement**                   | **Prioritas Awal** | **Rationale**                                                                                                       |
|-----------------------------------|--------------------|---------------------------------------------------------------------------------------------------------------------|
| **FR-01**                         | High               | Langsung menjawab pain point ketidakjelasan status bagi pemohon.                                                    |
| **FR-02**                         | High               | Menjadi dependency agar status yang ditampilkan dapat dipercaya dan ditelusuri.                                     |
| **FR-03**                         | High               | Menjaga kewenangan keputusan sesuai business rule.                                                                  |
| **FR-04**                         | High               | Mendukung tujuan utama pengajuan permohonan.                                                                        |
| **FR-05**                         | Medium             | Mendukung exception ketika data/lampiran belum sesuai.                                                              |
| **FR-06**                         | Medium             | Mendukung audit operasional, tetapi bergantung pada pencatatan perubahan status.                                    |
| **Kandidat: notifikasi otomatis** | Validasi dulu      | Menarik sebagai solusi, tetapi bukti discovery belum cukup untuk menyatakan kebutuhan spesifik terhadap notifikasi. |

# 9. Requirement Traceability Matrix (RTM)

RTM menghubungkan requirement dengan sumber, pain point, acceptance criteria, dan artefak berikutnya. Pada tahap Pertemuan 5, kolom model/desain dapat masih berupa rencana/TBD dan dilengkapi saat BPMN/use case/diagram lain tersedia.

![](media/image2.png)

Gambar 2. Contoh rantai traceability dari evidence sampai model berikutnya.

| **Req ID** | **Source**            | **Pain Point**                   | **Acceptance** | **Model/Next Artifact**       | **Status** |
|------------|-----------------------|----------------------------------|----------------|-------------------------------|------------|
| **FR-01**  | Interview M03         | PP-01 status tidak jelas         | AC-01, AC-02   | UC Cek Status / BPMN To-Be    | Draft      |
| **FR-02**  | Observasi O02         | PP-01                            | AC-03          | BPMN Update Status / Sequence | Draft      |
| **FR-03**  | BR-01 / prosedur      | Kewenangan keputusan             | AC-04          | Use Case / Access Control     | Validasi   |
| **FR-04**  | Opportunity OP-01     | Pengajuan perlu jalur yang jelas | AC-05          | BPMN / UC Ajukan Permohonan   | Draft      |
| **FR-05**  | Observasi O02 / BR-02 | Data tidak lengkap               | AC-06          | BPMN exception / Activity     | Draft      |

# 10. Baseline, Asumsi, dan Revision Notes

## 10.1 Baseline Draft

Versi 0.1 merupakan baseline awal untuk review. Perubahan setelah review BPMN, use case, atau stakeholder harus dicatat agar ID, istilah, dan hubungan antarartefak tetap konsisten.

## 10.2 Open Issues / TBD

| **ID**     | **Isu**                                                     | **Tindak Lanjut**                                          |
|------------|-------------------------------------------------------------|------------------------------------------------------------|
| **TBD-01** | Target waktu respons belum tersedia dari bukti.             | Validasi kebutuhan kinerja sebelum menetapkan angka.       |
| **TBD-02** | Sumber resmi BR-01/BR-02 pada kasus nyata belum ditetapkan. | Validasi dengan dokumen/prosedur resmi.                    |
| **TBD-03** | Model BPMN/use case/activity belum menjadi baseline.        | Lengkapi dan audit konsistensi pada pertemuan selanjutnya. |

## 10.3 Checklist Review SRS

- Setiap requirement memiliki ID dan sumber/rasional yang dapat ditelusuri.

- Functional requirement cukup jelas dan dapat diberi acceptance criteria.

- NFR tidak menggunakan kata ambigu tanpa konteks; angka yang belum didukung tidak dikarang.

- Business rule dipisahkan dari perilaku sistem dan memiliki sumber bisnis.

- Istilah aktor, status, dan objek bisnis konsisten pada seluruh bagian.

- RTM menunjukkan requirement yatim atau hubungan yang belum lengkap.

- Perubahan ID atau istilah disertai revision note.

# Lampiran A. Bukti Discovery Hipotetik

Lampiran ini hanya menunjukkan bagaimana contoh SRS menjaga jejak ke temuan awal. Bukti berikut bersifat hipotetik untuk pembelajaran.

| **Evidence ID** | **Jenis**        | **Potongan Temuan**                                                               | **Interpretasi Awal**                                            |
|-----------------|------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------|
| **M03**         | Wawancara        | "Saya biasanya bertanya ke petugas karena tidak tahu sudah sampai mana."          | Gejala ketidakjelasan status.                                    |
| **O02**         | Observasi        | Petugas membuka spreadsheet lokal untuk mengecek status sebelum menjawab pemohon. | Status tidak tersedia pada titik informasi pemohon.              |
| **P01**         | Dokumen/Prosedur | Keputusan akhir dilakukan oleh peran verifikator.                                 | Sumber kandidat untuk BR-01; harus divalidasi pada proyek nyata. |

# Referensi Acuan Pembelajaran

- Materi Pertemuan 5 IF21307 - Requirements Engineering: Functional/Non-Functional Requirements, Business Rules, Acceptance Criteria, Prioritas, RTM, dan Draft SRS.

- ISO/IEC/IEEE 29148:2018 (sebagaimana tercantum pada rujukan RPS).

- Sommerville - Software Engineering (sebagaimana tercantum pada rujukan RPS).

> **Catatan akhir: dokumen ini adalah contoh struktur dan isi untuk pembelajaran. Pada proyek mahasiswa, requirement, business rule, acceptance criteria, prioritas, serta traceability harus berasal dari hasil discovery dan bukti proyek masing-masing.**
