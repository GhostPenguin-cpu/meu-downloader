import os
from flask import Flask, render_template, request, send_from_directory, jsonify
import yt_dlp

app = Flask(__name__, template_folder='templates')

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/get_info', methods=['POST'])
def get_info():
    data = request.json
    video_url = data.get('link_video')
    if not video_url:
        return jsonify({'error': 'link faltando'}), 400
    try:
        ydl_opts = {'quiet': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title', 'Vídeo'),
                'thumb': info.get('thumbnail', '')
            })
    except:
        return jsonify({'error': 'erro ao buscar info'}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Buscando exatamente 'link_video'
        video_url = request.form.get('link_video')
        qualidade = request.form.get('qualidade', 'alta')

        if not video_url:
            return "Erro: Nenhuma URL foi enviada. Verifique se o campo no HTML tem name='link_video'.", 400

        try:
            formato = 'best' if qualidade == 'alta' else 'worst'
            ydl_opts = {
                'format': formato,
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)
        except Exception as e:
            return f"Erro no download: {str(e)}", 500
            
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
