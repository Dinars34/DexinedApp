import os
import glob
import subprocess
import streamlit as st
from PIL import Image

# ————————————————————————————————
# 1) Setup direktori dan session state
# ————————————————————————————————
DATA_DIR = "data"
FUSED_DIR = os.path.join("result", "BIPED2CLASSIC", "fused")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FUSED_DIR, exist_ok=True)

# Inisialisasi flag supaya hasil hanya tampil setelah proses
if "processed" not in st.session_state:
    st.session_state.processed = False

st.title("Deteksi jalan berlubang menggunakan DexiNed Egde Detection")

# ————————————————————————————————
# 2) Upload input
# ————————————————————————————————
upload = st.file_uploader("Unggah satu gambar jalan", type=["jpg","jpeg","png"])
if upload:
    st.session_state.uploaded_file = upload
else:
    # reset kalau user hapus input
    st.session_state.processed = False

# ————————————————————————————————
# 3) Tombol Proses
# ————————————————————————————————
if st.button("Memproses Gambar"):
    
    # 3.0 Validasi apakah gambar sudah diupload
    if not upload and "uploaded_file" not in st.session_state:
        st.error("❌ Silakan upload gambar terlebih dahulu sebelum memproses!")
    elif not upload and st.session_state.get("uploaded_file") is None:
        st.error("❌ Silakan upload gambar terlebih dahulu sebelum memproses!")
    else:
        # 3.1 Hapus semua file lama di DATA_DIR
        for f in glob.glob(os.path.join(DATA_DIR, "*")):
            os.remove(f)

        # 3.2 Simpan ulang file input (seharusnya hanya 1)
        input_path = os.path.join(DATA_DIR, st.session_state.uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(st.session_state.uploaded_file.getvalue())

        # 3.3 Hapus semua file lama di FUSED_DIR
        for f in glob.glob(os.path.join(FUSED_DIR, "*")):
            os.remove(f)

        # 3.4 Jalankan main.py (sesuaikan args jika perlu)
        with st.spinner("Sedang memproses gambar..."):
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True, text=True
            )
        
        if result.returncode == 0:
            st.success("Proses selesai 🎉")
            st.session_state.processed = True
        else:
            st.error("Proses gagal:")
            st.code(result.stderr)
            st.session_state.processed = False

# ————————————————————————————————
# 4) Tampilkan hasil jika sudah diproses
# ————————————————————————————————
if st.session_state.processed:
    # Cari file di fused (harusnya 1 file output)
    outputs = glob.glob(os.path.join(FUSED_DIR, "*.*"))
    if len(outputs) == 1:
        out_img = Image.open(outputs[0])
        st.subheader("Gambar Hasil")
        st.image(out_img, caption=os.path.basename(outputs[0]), use_container_width=True)
    elif len(outputs) > 1:
        st.warning(f"Ditemukan {len(outputs)} file, seharusnya hanya 1.")
    else:
        st.error("Tidak ada file output di folder fused.")