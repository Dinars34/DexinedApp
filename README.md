````markdown
# DexiNed Edge Detection App

## Deskripsi
Aplikasi ini menggunakan model DexiNed (Dense Edge eXtraction for Image NeD) untuk mendeteksi tepi pada citra. Dengan antarmuka web sederhana berbasis Streamlit, Anda dapat mengunggah gambar lokal dan melihat hasil deteksi tepi secara real time.

## Fitur
- Deteksi tepi menggunakan model DexiNed pre-trained
- Antarmuka web sederhana berbasis Streamlit
- Mendukung format gambar umum (PNG, JPEG, BMP)

## Prasyarat
- Python 3.7 atau lebih baru
- GPU (opsional, untuk inferensi lebih cepat) atau CPU

## Instalasi
1. Clone repository ini:
   ```bash
   git clone https://github.com/Dinars34/DexinedApp.git
   cd DexinedApp
   ````

2. Buat dan aktifkan virtual environment (opsional namun direkomendasikan):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Install semua dependency:

   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan

Jalankan aplikasi dengan perintah:

```bash
python app.py
```

<div style="text-align:center"><img src='figs/Pasted image (2).png' width=800>
</div>
```
