# Sistem Analisis Perlambatan Komputer

Sistem pakar berbasis **Teorema Bayes** untuk mendiagnosis penyebab penurunan performa komputer. Dibangun menggunakan Python dan Tkinter.

## Fitur

- Diagnosis berbasis 10 gejala umum perlambatan komputer
- Perhitungan probabilitas menggunakan Teorema Bayes
- Ranking penyebab dengan visualisasi progress bar
- Detail perhitungan formula Bayes secara transparan
- Rekomendasi perbaikan berdasarkan hasil diagnosis
- Riwayat diagnosis real-time

## Penyebab yang Dapat Dideteksi

| Kode | Penyebab | Prior |
|------|----------|-------|
| P01 | Penggunaan RAM Berlebihan | 0.30 |
| P02 | Kapasitas Penyimpanan Hampir Penuh | 0.25 |
| P03 | Terlalu Banyak Program Startup | 0.20 |
| P04 | Malware | 0.15 |
| P05 | Thermal Throttling | 0.10 |

## Gejala yang Dianalisis

| Kode | Gejala |
|------|--------|
| G01 | Proses booting berlangsung lama |
| G02 | Penggunaan RAM lebih dari 90% |
| G03 | Disk Usage mencapai 100% |
| G04 | Banyak aplikasi berjalan saat startup |
| G05 | Aplikasi sering mengalami freeze |
| G06 | Membuka aplikasi terasa lambat |
| G07 | Kapasitas penyimpanan hampir penuh |
| G08 | Antivirus mendeteksi malware |
| G09 | Suhu prosesor tinggi |
| G10 | Kipas pendingin berputar sangat cepat |

## Metode

Sistem menggunakan **Teorema Bayes** untuk menghitung probabilitas posterior setiap penyebab berdasarkan gejala yang dipilih:

```
P(Pᵢ|G) = [P(Pᵢ) × ∏P(Gⱼ|Pᵢ)] / Σ[P(Pₖ) × ∏P(Gⱼ|Pₖ)]
```

Setiap penyebab memiliki nilai **prior probability** dan **likelihood** terhadap masing-masing gejala yang telah ditentukan berdasarkan basis pengetahuan pakar.

## Cara Menjalankan

```bash
python bayes_diagnosis.py
```

### Prasyarat

- Python 3.x
- Tkinter (sudah termasuk dalam instalasi standar Python)

## Screenshot

### Halaman Utama
![Welcome Screen](docs/welcome.png)

### Hasil Diagnosis
![Diagnosis Result](docs/result.png)

## Teknologi

- **Bahasa:** Python
- **GUI:** Tkinter
- **Metode:** Teorema Bayes (Sistem Pakar)

## Lisensi

MIT License
