from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Configuração da pasta de downloads
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        link = request.form.get("link")
        qualidade = request.form.get("qualidade")

        try:
            # Nome base para o arquivo
            video_filename = "download_video"
            output_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

            # Define a regra de qualidade
            if qualidade == "alta":
                format_opt = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            else:
                format_opt = 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst'

            ydl_opts = {
                'format': format_opt,
                'outtmpl': f'{output_path}.%(ext)s',
                'overwrites': True,
                'nocheckcertificate': True,
                'quiet': True,
                'addheader': [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                ext = info.get('ext', 'mp4')
                arquivo_final = f"{output_path}.{ext}"

            return send_file(arquivo_final, as_attachment=True)

        except Exception as e:
            return f"<h2>Erro: {e}</h2><a href='/'>Voltar</a>"

    return render_template("index.html")

# Rota para buscar a capa do vídeo sem baixar
@app.route("/get_info", methods=["POST"])
def get_info():
    data = request.get_json()
    link = data.get("link")
    try:
        ydl_opts = {'quiet': True, 'nocheckcertificate': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return jsonify({
                'title': info.get('title', 'Vídeo'),
                'thumb': info.get('thumbnail', '')
            })
    except:
        return jsonify({'error': 'Link inválido'}), 400

if __name__ == "__main__":
    app.run(debug=True)