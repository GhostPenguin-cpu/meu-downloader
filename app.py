import os
from flask import Flask, render_template, request, send_from_directory
import yt_dlp

app = Flask(__name__)

# Configuração da pasta de downloads (Caminho absoluto para o Render)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    if not video_url:
        return "Por favor, insira uma URL válida.", 400

    try:
        ydl_opts = {
            # Baixa na melhor qualidade que já tenha áudio e vídeo juntos (evita erro de ffmpeg)
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            # Pegamos apenas o nome do arquivo, sem o caminho da pasta
            base_filename = os.path.basename(filename)

        return send_from_directory(DOWNLOAD_FOLDER, base_filename, as_attachment=True)

    except Exception as e:
        return f"Erro ao baixar o vídeo: {str(e)}", 500

if __name__ == '__main__':
    # No seu PC usa a porta 5000, no Render ele escolhe a porta sozinho
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
