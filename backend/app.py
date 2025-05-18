import os
import requests # Using requests for HTTP calls
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq # Using the groq library as per requirements.txt

# Muat variabel dari file .env
load_dotenv()

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')

# Konfigurasi CORS
# Mengizinkan permintaan dari semua origin ke endpoint /chat
# Secara eksplisit mengizinkan metode POST dan OPTIONS, serta header Content-Type
CORS(app, resources={
    r"/chat": {
        "origins": "*", 
        "methods": ["POST", "OPTIONS"], 
        "allow_headers": ["Content-Type"]
    }
})

# Ambil API key Groq dari variabel lingkungan
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("Peringatan: GROQ_API_KEY tidak disetel. Silakan set di file .env")

# Inisialisasi klien Groq
# Pastikan Anda telah menginstal pustaka Groq: pip install groq
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Gagal menginisialisasi klien Groq: {e}")
    groq_client = None

ADMIN_FORUM_PERTANIAN_PERSONA = """
Anda adalah admin forum pertanian yang sangat membantu dan berpengetahuan luas. 
Nama Anda adalah "AgroBot".
Anda selalu merespons dalam bahasa Indonesia.
Tugas Anda adalah memberikan informasi yang akurat, saran praktis, dan jawaban yang jelas terkait berbagai topik pertanian, 
termasuk teknik budidaya, pengendalian hama dan penyakit, pemilihan bibit, pemupukan, irigasi, panen dan pasca-panen, 
serta isu-isu pertanian modern dan berkelanjutan.
Jaga agar respons Anda tetap sopan, profesional, dan mudah dipahami oleh petani dari berbagai tingkat pengalaman.
Jika pertanyaan di luar topik pertanian, tolak dengan sopan dan arahkan kembali ke topik pertanian.
"""

@app.route('/')
def index():
    """Menyajikan halaman utama chat."""
    return render_template('index.html')

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Menerima pesan dari pengguna dan mengembalikan respons dari Groq LLM."""
    if request.method == 'OPTIONS':
        # Ini adalah preflight request. Flask-CORS akan menambahkan header yang sesuai
        # berdasarkan konfigurasi di atas. Kita cukup mengembalikan respons OK.
        return jsonify({"status": "ok", "message": "Preflight OK"}), 200

    # Jika ini adalah permintaan POST, lanjutkan dengan logika chat
    if not groq_client:
        return jsonify({"error": "Klien Groq tidak terinisialisasi. Periksa API Key Anda."}), 500
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY tidak dikonfigurasi di server."}), 500

    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({"error": "Pesan tidak boleh kosong."}), 400

        print(f"Pesan diterima dari pengguna: {user_message}")

        # Membuat prompt untuk Groq
        messages = [
            {
                "role": "system",
                "content": ADMIN_FORUM_PERTANIAN_PERSONA
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        # Mengirim permintaan ke Groq API menggunakan pustaka groq
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192", # Model diperbarui ke llama3-8b-8192
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )

        bot_response = chat_completion.choices[0].message.content
        print(f"Respons dari Groq: {bot_response}")

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Terjadi kesalahan saat menghubungi Groq API atau memproses permintaan: {e}")
        # Menyertakan detail error dari Groq jika ada
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'json'):
            try:
                error_detail = e.response.json()
                if isinstance(error_detail, dict) and 'error' in error_detail:
                    error_message = f"{str(e)} - Detail: {error_detail['error']}"
            except: # Abaikan jika parsing JSON gagal
                pass
        return jsonify({"error": f"Maaf, terjadi kesalahan internal: {error_message}"}), 500

if __name__ == '__main__':
    # Pastikan untuk menyetel debug=False di lingkungan produksi
    app.run(debug=True, port=5000) 