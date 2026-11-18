# Instruksi Revisi Dokumen SDD v1.1 (Eksekusi AI Agent)

**Target Dokumen:** `Tugas_3_KelompokXX_AnalysisModels_v1.1.docx` (atau sumber `.md` penyusunnya)  
**Cakupan Tugas:** Penyuntingan teks narasi, tabel kontrak operasi, aturan *Integrity Constraint* (IC), matriks RTM, dan pembersihan sisa *template* v1.0. *(Catatan: File gambar diagram tidak diubah pada tahap ini).*

---

## 1. Penyelarasan Parameter Operasi (Bab 3 vs Bab 6.2)

Samakan tanda tangan (*signature*) dan daftar parameter operasi antara tabel skenario interaksi di **Bab 3 (Tabel 3.2–3.5)** dengan tabel kontrak operasi di **Bab 6.2** agar konsisten 100%:

| Kelas & Nama Operasi | Standar Parameter yang Harus Dipakai | Lokasi Perubahan |
| :--- | :--- | :--- |
| `TIKET_PESANAN.ajukan(...)` | `ajukan(judul_publikasi, kanal_tujuan, jenis_konten, tanggal_target_tayang, deskripsi_brief, is_rush_order, alasan_darurat)` | Tabel 3.2 (Main Flow langkah 20) & Tabel Bab 6.2 |
| `TIKET_PESANAN.validasiSLA(...)` | `validasiSLA(kanal_tujuan, jenis_konten) : Boolean` | Tabel Bab 6.2 (tambahkan 2 parameter yang sebelumnya kosong) |
| `TIKET_PESANAN.setujuiBrief(...)` | `setujuiBrief(id_pengguna_admin, tanggal_verifikasi)` | Tabel Bab 6.2 (sesuaikan dari `id_admin`) |
| `TIKET_PESANAN.tugaskan(...)` | `tugaskan(id_eksekutor, waktu_penugasan)` | Tabel Bab 6.2 (sesuaikan dari `id_eksekutor`) |
| `PENGGUNA.cekPeran(...)` | `cekPeran(id_pengguna) : Enumerasi` | Tabel Bab 6.2 (tambahkan parameter `id_pengguna`) |
| `PENGGUNA.hitungTiketAktif(...)` | `hitungTiketAktif(id_eksekutor) : Angka` | Tabel Bab 6.2 (tambahkan parameter `id_eksekutor`) |
| `DRAF_KARYA.versiBerikutnya(...)` | `versiBerikutnya(id_tiket) : Teks` | Tabel Bab 6.2 (tambahkan parameter `id_tiket`) |
| `DRAF_KARYA.unggahDraf(...)` | `unggahDraf(id_tiket, versi_draf, file_path_preview, tautan_preview_video, catatan_draf)` | Tabel Bab 6.2 (sesuaikan nama & jumlah 5 parameter) |
| `RIWAYAT_REVISI.catatRevisi(...)` | `catatRevisi(id_tiket, poin_revisi, revisi_ke) : Angka` | Tabel Bab 6.2 (sesuaikan dari `catatRevisi(poin)`) |
| `RIWAYAT_PENUGASAN.catatPenugasan(...)` | `catatPenugasan(id_tiket, id_eksekutor, jenis_penugasan, alasan_mutasi) : Angka` | Tabel Bab 6.2 (sesuaikan dari `catatPenugasan(jenis, alasan)`) |

---

## 2. Koreksi Keterangan Gambar UML Class Diagram (Bab 6.1)

* **Lokasi:** Paragraf keterangan tepat di bawah **Gambar 6.1** (Bab 6.1).
* **Teks Lama:**  
  > *"Kunci tamu ERD diwakili asosiasi dan karena itu tidak muncul sebagai atribut kelas, kecuali id_pengguna, id_tiket, id_draf, dan id_revisi yang tetap ditulis sebagai pengenal objek."*
* **Teks Baru (Perbaikan):**  
  > *"Relasi antar-kelas diwakili oleh garis komposisi (`*--`) dan asosiasi (`-->`), sementara atribut kunci tamu (FK) seperti `id_kementerian`, `id_pemohon`, `id_eksekutor`, `id_tiket`, dan `id_staf_medsos` tetap dicantumkan secara eksplisit pada kompartemen atribut kelas untuk memudahkan penelusuran langsung ke skema basis data logis pada Bab 4.2."*

---

## 3. Penyempurnaan Kontrak Operasi & Integrity Constraint (Bab 5.2 & Bab 6.2)

1. **Perbaikan Postcondition `TIKET_PESANAN.setujuiBrief()` (Bab 6.2):**
   * **Teks Lama:** `Post: tanggal_verifikasi terisi dan status menjadi Assigned setelah penugasan (IC-09).`
   * **Teks Baru:** `Post: tanggal_verifikasi terisi dan tiket dinyatakan layak untuk masuk ke tahap penugasan eksekutor (IC-09).` *(Alasan: perubahan status menjadi `Assigned` dilakukan oleh `tugaskan()`, bukan `setujuiBrief()`).*

2. **Perbaikan Precondition `PUBLIKASI_KONTEN.catatPublikasi()` (Bab 6.2):**
   * **Teks Lama:** `Pre: status tiket ∈ {Ready to Post, Published}; url tidak kosong; satu tiket hanya boleh punya satu catatan publikasi.`
   * **Teks Baru:** `Pre: status tiket = Ready to Post; url tidak kosong; satu tiket hanya boleh punya satu catatan publikasi.` *(Alasan: status baru berubah menjadi `Published` setelah `tutupTiket()` dijalankan).*

3. **Perluasan Cakupan Beban Kerja Aktif pada `IC-08` (Bab 5.2) & `PENGGUNA.hitungTiketAktif()` (Bab 6.2):**
   * **Teks Lama:** `Jumlah tiket berstatus In Progress per id_eksekutor ≤ 3; penugasan ke-4 memicu peringatan wajib konfirmasi Admin.`
   * **Teks Baru:** `Jumlah tiket aktif dengan status_tiket ∈ {Assigned, In Progress, Revision} per id_eksekutor ≤ 3; penugasan ke-4 memicu peringatan wajib konfirmasi Admin.`
   * *(Terapkan penyesuaian himpunan status yang sama pada Postcondition `PENGGUNA.hitungTiketAktif()` di Bab 6.2 dan Langkah 5 Tabel 7.3 Walkthrough).*

---

## 4. Pembersihan Sisa Teks v1.0 & Placeholder Dokumen

Lakukan pencarian dan penggantian (*find & replace*) pada bagian-bagian berikut:

1. **Judul Sub-bab 7.1:**
   * Ubah `7.1 Requirements Traceability Matrix (Minggu selanjutnya v1.1)` menjadi `7.1 Requirements Traceability Matrix (RTM)`.
2. **Paragraf Pengantar Bab 7.1:**
   * Hapus kalimat: *"Kolom BPMN/Activity bertanda 'belum tersedia' mengikuti catatan ketersediaan artefak pada Bab 1.2."*
   * Ganti dengan: *"Seluruh kolom keterlacakan hulu (BPMN, Use Case, Activity Diagram) hingga hilir (Sequence Diagram, ERD/IC, dan Kelas Domain) telah terisi lengkap sesuai baseline v1.1."*
3. **Baris `FR-01` pada Tabel RTM (Bab 7.1):**
   * Pada kolom **Activity Diagram**, ubah `AD-00` menjadi `di luar cakupan SDD (Pertemuan 12)`.
4. **Lampiran B (Pembagian Kontribusi Anggota Tim):**
   * Hapus kalimat instruksi: *"Sesuaikan bila ada pergeseran tugas antar-anggota."*
   * Ubah teks `"pada tahap v1.0"` menjadi `"pada tahap v1.0 dan v1.1"`.
   * Ubah header kolom tabel dari `Kontribusi pada SDD v1.0` menjadi `Kontribusi pada SDD v1.0 & v1.1`.
5. **Placeholder Nomor Kelompok:**
   * Ganti seluruh kemunculan `KelompokXX` (pada header/catatan dokumen dan Lampiran C) dengan identitas/nomor kelompok resmi Anda.

---

## 5. Koreksi Keterangan Teks Lampiran D.1 (BPMN-01)

* **Lokasi:** Paragraf di bawah gambar **D.1 BPMN To-Be** (Lampiran D.1).
* **Teks Lama:** `Empat lane aktor ditambah data store.`
* **Teks Baru:** `Lima swimlane proses/aktor (Klien, Admin, Eksekutor, Tinjauan Klien, dan Staf Medsos) ditambah satu data store.`

---

## 6. Pembaruan Defect Log (Bab 7.5) & Revision Log (Lampiran A)

Tambahkan entri baru pada **Tabel 7.5 (Defect Log)** dan **Lampiran A (Revision Log)** untuk mencatat perbaikan di atas agar audit *traceability* tetap tercatat:

* **ID Defect Baru (`DEF-09` atau catatan audit lanjutan):**
  * **Temuan:** Ketidaksesuaian daftar parameter operasi antara Sequence Diagram (Bab 3) dan Kontrak Operasi (Bab 6.2), kontradiksi keterangan atribut FK pada Bab 6.1, celah status aktif pada IC-08, serta sisa teks draf v1.0 pada Bab 7.1 dan Lampiran B.
  * **Tindakan Perbaikan:** Menyamakan seluruh parameter operasi di Bab 6.2 dengan pesan di Bab 3, merevisi keterangan Gambar 6.1, memperluas status beban aktif IC-08 menjadi `{Assigned, In Progress, Revision}`, dan membersihkan sisa teks v1.0.
  * **Status:** `Selesai`.