import os
from flask import Flask, render_template, request, send_from_directory
import yt_dlp

app = Flask(__name__, template_folder='templates')

# Pasta temporária para salvar os downloads
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('url')
        
        if not video_url:
            return "Erro: Nenhuma URL foi enviada.", 400

        try:
            # Configurações para aceitar TikTok, Insta, YT e FB
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'noplaylist': True,
                # O User-Agent simula um navegador real para evitar bloqueios
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extrai os dados e faz o download físico para a pasta 'downloads'
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Envia o arquivo baixado para o navegador do usuário
                return send_from_directory(
                    DOWNLOAD_FOLDER, 
                    os.path.basename(filename), 
                    as_attachment=True
                )

        except Exception as e:
            return f"Erro ao processar vídeo das redes sociais: {str(e)}", 500
            
    return render_template('index.html')

if __name__ == '__main__':
    # O Render usa a variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
