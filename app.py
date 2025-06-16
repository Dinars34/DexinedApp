import os
import glob
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = 'secret_key'  # Ganti dengan secret key yang kuat

# Konfigurasi direktori
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FUSED_DIR = os.path.join(BASE_DIR, 'result', 'BIPED2CLASSIC', 'avg')

# Pastikan direktori ada
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FUSED_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Bersihkan direktori lama
                for f in glob.glob(os.path.join(DATA_DIR, '*')):
                    os.remove(f)
                for f in glob.glob(os.path.join(FUSED_DIR, '*')):
                    os.remove(f)
                
                # Simpan file baru
                filename = secure_filename(file.filename)
                input_path = os.path.join(DATA_DIR, filename)
                file.save(input_path)
                
                session['uploaded_file'] = filename
                session['processed'] = False
                return redirect(url_for('index'))
    
    # Handle proses gambar
    if 'process' in request.form and 'uploaded_file' in session:
        input_path = os.path.join(DATA_DIR, session['uploaded_file'])
        
        try:
            # Jalankan proses utama
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True,
                text=True,
                cwd=BASE_DIR
            )
            
            if result.returncode == 0:
                session['processed'] = True
            else:
                return render_template('index.html', error=result.stderr)
        except Exception as e:
            return render_template('index.html', error=str(e))
    
    # Periksa hasil proses
    processed_image = None
    if session.get('processed'):
        outputs = glob.glob(os.path.join(FUSED_DIR, '*.*'))
        if outputs:
            processed_image = os.path.basename(outputs[0])
    
    return render_template(
        'index.html',
        uploaded_file=session.get('uploaded_file'),
        processed=session.get('processed'),
        processed_image=processed_image
    )

@app.route('/data/<filename>')
def data_file(filename):
    return send_from_directory(DATA_DIR, filename)

@app.route('/result/<filename>')
def result_file(filename):
    return send_from_directory(FUSED_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
