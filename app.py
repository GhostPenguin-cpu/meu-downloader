import os
from flask import Flask, render_template, request, send_from_directory
import yt_dlp

# Isso força o Flask a entender que a pasta templates está na mesma pasta que este arquivo
app = Flask(__name__, template_folder='templates')

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    # Adicionamos um try/except aqui para o erro não ser uma tela branca
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Erro: O arquivo index.html não foi encontrado na pasta templates. Detalhe: {e}"

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    if not video_url:
        return "URL vazia", 400

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)

    except Exception as e:
        return f"Erro no download: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
