import os
from flask import Flask, render_template, request, send_from_directory
import yt_dlp

app = Flask(__name__, template_folder='templates')

# Pasta de downloads
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('url')
        if not video_url:
            return "Erro: URL vazia", 400

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
            
    # Se for GET, apenas mostra a página
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
