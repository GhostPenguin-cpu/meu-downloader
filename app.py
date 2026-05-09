@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifique se o nome aqui coincide com o 'name' do input no HTML
        video_url = request.form.get('url') 
        
        if not video_url:
            return "Erro: URL vazia. O formulário não enviou o link corretamente.", 400

        try:
            ydl_opts = {
                'format': 'best',
                # O TikTok às vezes requer configurações específicas de cookies ou user-agent, 
                # mas o básico do yt-dlp costuma resolver:
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)

        except Exception as e:
            return f"Erro ao processar link do TikTok: {str(e)}", 500
            
    return render_template('index.html')
