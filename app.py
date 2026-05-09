import os
import uuid
from flask import Flask, render_template, request, send_from_directory, jsonify
import yt_dlp

app = Flask(__name__, template_folder='templates')

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/get_info', methods=['POST'])
def get_info():
    data = request.json
    video_url = data.get('link')
    try:
        ydl_opts = {'quiet': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({'title': info.get('title'), 'thumb': info.get('thumbnail')})
    except: return jsonify({'error': 'erro'}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Pega o link do campo 'link' do HTML
        video_url = request.form.get('link')
        if not video_url:
            return "Erro: URL vazia. O formulário não enviou o link.", 400

        try:
            # Nome único para evitar erros de caracteres especiais no servidor
            id_unico = str(uuid.uuid4())
            
            ydl_opts = {
                # Força o melhor formato MP4 disponível
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{id_unico}.%(ext)s'),
                'noplaylist': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                # Nome do arquivo físico no servidor
                filename = f"{id_unico}.mp4"
                
                # Nome que o usuário verá ao salvar (limpo de símbolos)
                display_name = "".join([c for c in info.get('title', 'video') if c.isalnum() or c==' ']).strip()
                display_name = f"{display_name}.mp4"
                
                return send_from_directory(
                    DOWNLOAD_FOLDER, 
                    filename, 
                    as_attachment=True,
                    download_name=display_name,
                    mimetype='video/mp4'
                )
        except Exception as e:
            return f"Erro: {str(e)}", 500
            
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
