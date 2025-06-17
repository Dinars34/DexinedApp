import os
import glob
import subprocess
import streamlit as st
from PIL import Image

# ————————————————————————————————
# 1) Setup direktori dan session state
# ————————————————————————————————
DATA_DIR = "data"
FUSED_DIR = os.path.join("result", "BIPED2CLASSIC", "avg")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FUSED_DIR, exist_ok=True)

if "processed" not in st.session_state:
    st.session_state.processed = False

st.title("Deteksi Jalan Berlubang Menggunakan Edge Detection")

# ————————————————————————————————
# 2) Upload input
# ————————————————————————————————
upload = st.file_uploader("Unggah satu gambar jalan", type=["jpg","jpeg","png"])
if upload:
    st.session_state.uploaded_file = upload
    st.session_state.processed = False

# ————————————————————————————————
# 3) Tombol Proses
# ————————————————————————————————
if st.button("Proses dan Bandingkan"):
    if "uploaded_file" not in st.session_state or st.session_state.uploaded_file is None:
        st.error("❌ Silakan upload gambar terlebih dahulu sebelum memproses!")
    else:
        # Bersihkan folder input dan output
        for f in glob.glob(os.path.join(DATA_DIR, "*")):
            os.remove(f)
        for f in glob.glob(os.path.join(FUSED_DIR, "*")):
            os.remove(f)

        # Simpan gambar input
        input_path = os.path.join(DATA_DIR, st.session_state.uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(st.session_state.uploaded_file.getvalue())

        # Jalankan main.py untuk menghasilkan output
        with st.spinner("Memproses gambar..."):
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True, text=True
            )

        if result.returncode == 0:
            st.success("Proses selesai 🎉")
            st.session_state.input_path = input_path
            # Dapatkan file output (asumsi 1 gambar)
            outputs = glob.glob(os.path.join(FUSED_DIR, "*.*"))
            if outputs:
                st.session_state.output_path = outputs[0]
                st.session_state.processed = True
            else:
                st.error("❌ Output tidak ditemukan di folder fused.")
        else:
            st.error("Proses gagal:")
            st.code(result.stderr)

# ————————————————————————————————
# 4) Tampilkan perbandingan jika sudah diproses
# ————————————————————————————————
if st.session_state.processed:
    # Muat gambar asli dan hasil
    img_orig = Image.open(st.session_state.input_path)
    img_processed = Image.open(st.session_state.output_path)

    st.subheader("Perbandingan Gambar Asli dan Hasil Deteksi Edge")
    col1, col2 = st.columns(2)
    with col1:
        st.image(img_orig, caption="Asli", use_container_width=True)
    with col2:
        st.image(img_processed, caption="Hasil Deteksi", use_container_width=True)
