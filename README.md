# Simulator Komputasi Kuantum

Simulator komputasi kuantum berbasis Python yang memungkinkan Anda untuk bereksperimen dengan algoritma dan konsep kuantum menggunakan perangkat keras klasik. Simulator ini dilengkapi dengan visualisasi interaktif dan analisis statistik mendalam.

## Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip package manager

### Paket yang Diperlukan
```bash
# Install paket yang diperlukan
pip install qiskit qiskit-aer numpy rich

# Verifikasi instalasi dengan menjalankan test
python3 test_install.py
```

## Fitur Utama

### 1. Operasi Kuantum Dasar
- **Manajemen Qubit**: Membuat dan memanipulasi sistem multi-qubit
- **Gerbang Kuantum**:
  - Gerbang Hadamard (H) untuk menciptakan superposisi
  - Gerbang CNOT untuk operasi entanglement
  - Gerbang rotasi fase (RZ) untuk manipulasi fase
- **Pengukuran**: Kemampuan untuk mengukur qubit secara individual atau keseluruhan

### 2. Protokol Kuantum
- **Bell Pair**: Implementasi entanglement kuantum
- **Teleportasi Kuantum**: Protokol lengkap untuk teleportasi keadaan
- **Sirkuit Kustom**: Pembuatan sirkuit quantum sesuai kebutuhan

### 3. Visualisasi dan Analisis
- **Distribusi Pengukuran**: Histogram ASCII interaktif
- **Diagram Sirkuit**: Representasi visual sirkuit kuantum
- **Analisis Statistik**: Metrik performa dan kualitas
- **State Vector**: Representasi keadaan kuantum

## Cara Penggunaan

### 1. Demonstrasi Bell Pair

```python
from pyquant import QuantumSimulator

# Membuat Bell Pair
sim = QuantumSimulator(2)
sim.create_bell_pair()
sim.measure_all()
results = sim.run(shots=1000)
```

Output akan menampilkan:
```
=== Bell Pair Demonstration ===

Measurement Distribution:
|00⟩ ████████████ 50.2% (502)
|11⟩ ████████████ 49.8% (498)

Quantum Circuit:
q₀: ──[H]──[●]──
          │
q₁: ─────[X]──

Statistical Analysis:
┌──────────────────┬─────────┐
│ Metric           │ Value   │
├──────────────────┼─────────┤
│ Total Measures   │ 1000    │
│ Unique States    │ 2       │
│ Fidelity         │ 0.998   │
└──────────────────┴─────────┘
```

### 2. Demonstrasi Teleportasi Kuantum

```python
# Teleportasi keadaan kuantum
sim = QuantumSimulator(3)
state_to_teleport = [1, 0.5]  # [amplitudo, fase]
sim.quantum_teleportation(state_to_teleport)
results = sim.run(shots=1000)
```

Output akan menampilkan:
```
=== Quantum Teleportation Demonstration ===

Measurement Distribution:
|000⟩ ██████████ 33.3% (333)
|011⟩ ██████████ 33.4% (334)
|101⟩ ██████████ 33.3% (333)

Quantum Circuit:
q₀: ──[X]──[H]──[M]────
q₁: ──[H]──[●]──[M]────
          │
q₂: ─────[X]─────────

Statistical Analysis:
┌──────────────────┬─────────┐
│ Metric           │ Value   │
├──────────────────┼─────────┤
│ Total Measures   │ 1000    │
│ Unique States    │ 3       │
│ Max Probability  │ 0.334   │
└──────────────────┴─────────┘
```

### 3. Menjalankan Semua Demonstrasi

```bash
python3 examples.py
```

Output lengkap akan menampilkan:
1. Header dengan timestamp
2. Demonstrasi Bell Pair
3. Demonstrasi Teleportasi
4. Ringkasan keseluruhan

## Interpretasi Hasil

### 1. Bell Pair
- **Distribusi Ideal**: 50% |00⟩ dan 50% |11⟩
- **Fidelity**: Nilai mendekati 1.0 menunjukkan entanglement yang baik
- **Unique States**: Seharusnya hanya 2 state (|00⟩ dan |11⟩)

### 2. Teleportasi
- **Distribusi**: Seharusnya seimbang antara state yang mungkin
- **Max Probability**: Mengindikasikan keberhasilan teleportasi
- **State Count**: Jumlah state yang muncul sesuai protokol

## Tips dan Troubleshooting

### 1. Optimasi Display
- Gunakan terminal yang mendukung Unicode
- Atur ukuran terminal minimal 80x24
- Pastikan font terminal mendukung karakter ASCII extended

### 2. Penanganan Error Umum
```python
# Jika hasil tidak muncul
console.print("Results:", results, markup=True)

# Jika visualisasi rusak
console.width = 100  # Set lebar console
```

### 3. Kustomisasi Output
```python
# Mengubah jumlah shots
results = sim.run(shots=2000)  # Default 1000

# Mengubah format histogram
bars = "■" * int(percentage / 2)  # Karakter alternatif
```

## Batasan dan Pertimbangan

### 1. Keterbatasan Perangkat Keras
- Simulasi terbatas pada jumlah qubit (~25-30 qubit)
- Memori yang dibutuhkan meningkat eksponensial
- Waktu komputasi bertambah dengan kompleksitas sirkuit

### 2. Akurasi Simulasi
- Menggunakan presisi floating-point
- Dekoherensi tidak disimulasikan
- Ideal quantum gates (tanpa noise)

## Pengembangan Lanjutan

### 1. Menambah Protokol Baru
```python
def custom_protocol(self):
    # Implementasi protokol kustom
    pass
```

### 2. Visualisasi Tambahan
```python
# Menambah format visualisasi
def show_bloch_sphere():
    # Implementasi visualisasi Bloch sphere
    pass
```

### 3. Metrik Analisis
```python
# Menambah metrik analisis
def calculate_advanced_stats():
    # Implementasi statistik lanjutan
    pass
```

## Dukungan dan Kontribusi

### Mendapatkan Bantuan
1. Buat issue di repositori
2. Dokumentasikan error dengan detail
3. Sertakan output lengkap

### Berkontribusi
1. Fork repositori
2. Buat branch untuk fitur baru
3. Submit pull request dengan deskripsi lengkap

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail.