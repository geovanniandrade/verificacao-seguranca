# GuiPhish 🔐

Ferramenta educacional para laboratório de conscientização em segurança, demonstrando riscos associados a permissões de navegador, geolocalização e engenharia social.

<img width="716" height="795" alt="image" src="https://github.com/user-attachments/assets/5f4e025b-fd7a-47ef-8769-6bb63a44a424" />

---

## 🎯 Objetivo

Simular um cenário controlado onde o usuário concede permissões sensíveis do navegador, como câmera, localização e informações de e-mail, demonstrando como decisões aparentemente simples podem levar à exposição de dados.

Além disso, a ferramenta realiza **análise comportamental**, classificando o nível de risco com base no tempo de resposta do usuário.

---

## ⚙️ Tecnologias

- HTML
- CSS
- JavaScript
- Python
- Flask
- Cloudflared
- Kali Linux

---

## 🔄 Fluxo de funcionamento

1. O servidor Flask é iniciado no Kali Linux
2. O usuário escolhe um modo no menu da ferramenta
3. O Cloudflared gera um link HTTPS temporário
4. O usuário acessa o link
5. A página apresenta opções de simulação
6. O usuário interage (câmera, localização ou templates)
7. Os eventos são registrados em tempo real
8. O dashboard exibe os dados com análise de risco
9. Relatórios podem ser gerados localmente
10. A simulação é finalizada com conscientização do usuário

---

## 🧠 Funcionalidades principais

- 📸 Captura de câmera (com consentimento)
- 🌍 Captura de localização
- 📧 Simulação de e-mail (sem coleta de senha)
- 🎯 Templates de phishing simulados
- ⏱️ Análise de tempo de resposta
- 🔴 Classificação de risco:
  - Alto risco (< 2s)
  - Médio risco (2–5s)
  - Consciente (> 5s)
- 📊 Dashboard estilo SOC
- 📺 Modo demonstração ao vivo (auto refresh)
- 📚 Página educativa (`/learn`)
- 🧾 Geração de relatórios
- 🧹 Limpeza de evidências locais

---

## 🐍 Backend Flask

O Flask é responsável por:

- Servir páginas HTML (templates e páginas educativas)
- Receber eventos via `/evento`
- Receber imagens via `/capture`
- Classificar risco comportamental
- Registrar logs em `data/logs/eventos.jsonl`
- Salvar fotos em `data/fotos/`
- Gerar relatórios em `data/reports/`
- Disponibilizar dashboard protegido por login

---

## 🧪 Instalação e execução

### 1. Atualizar o sistema

```bash
sudo apt update
```

### 2. Instalar dependências
```bash
sudo apt install git python3-flask -y
git clone https://github.com/geovanniandrade/verificacao-seguranca.git
```

### 3. Acessar o projeto
```bash
cd ~/verificacao-seguranca
```

### 4. Executar o servidor Flask
```bash
python3 core/server.py
```

### 🔐 Proteção de dados locais

O projeto possui um script chamado setup_security.sh para preparar o ambiente local com mais segurança.

Esse script:
```bash
Cria/atualiza .gitignore
Impede envio de dados sensíveis ao GitHub
Cria pastas locais:
data/fotos/
data/logs/
data/reports/
Aplica permissão chmod 700
```
Executar:
```bash
chmod +x setup_security.sh
./setup_security.sh
```

### 📋 Menu da ferramenta
```bash
1) 📸 Testar permissão de câmera/localização
2) 🎯 Escolher template de simulação
3) 📊 Dashboard / login
4) 🧾 Gerar relatório do lab
5) 🧹 Limpar evidências locais
6) 🛑 Sair
```

### 🌐 Expor o lab com HTTPS
```bash
cloudflared tunnel --url http://127.0.0.1:10000
```
Exemplo de link:
```bash
https://exemplo.trycloudflare.com
```

### 📊 Dashboard

Acesse:
```bash
https://SEU-LINK.trycloudflare.com/login
```
<img width="1022" height="763" alt="image" src="https://github.com/user-attachments/assets/1ec7ca5c-955c-4798-8f9b-cdaf5a9c6719" />

Credenciais padrão:
```bash
Usuário: admin
Senha: guiphish
```
<img width="2189" height="1168" alt="image" src="https://github.com/user-attachments/assets/b9a939f8-4aaf-4384-9d43-f1390449fed3" />


Também é possível alterar via variável de ambiente:
```bash
DASHBOARD_USER=admin DASHBOARD_PASS=SenhaForte python3 core/server.py
```

### 🎯 Templates disponíveis
```bash
💼 Rede profissional
🔒 Conta bloqueada
🛡️ Atualização de segurança
📧 Simulação de e-mail
```
<img width="543" height="503" alt="image" src="https://github.com/user-attachments/assets/527c4868-8bc2-4208-9e8a-fbdf021bc48c" />


### 📚 Página educativa

Acesse:
```bash
https://SEU-LINK.trycloudflare.com/learn
```
Conteúdo:
```bash
O que é phishing
Sinais de alerta
Boas práticas
Checklist de segurança
```

### 📧 Simulação de e-mail
```bash
https://SEU-LINK.trycloudflare.com/email
```
Registra apenas domínio — não coleta dados sensíveis.

### 📸 Validar fotos capturadas
```bash
ls data/fotos
xdg-open data/fotos
```

### 🌍 Validar logs
```bash
tail -n 10 data/logs/eventos.jsonl
```
### 🧾 Relatórios

Gerados via menu (opção 4):
```bash
data/reports/
```

### 🧹 Limpeza de evidências

Menu opção 5:

Remove:
```bash
fotos
logs
relatórios
```

### ⚠️ Uso ético

Este projeto deve ser utilizado apenas em:
```bash
ambientes controlados
treinamentos autorizados
fins educacionais

Nunca utilize sem consentimento.
```
## 🛡️ Aprendizados

- Engenharia social
- Phishing awareness
- Permissões do navegador
- Geolocalização via browser
- WebRTC
- Backend com Flask
- Monitoramento de eventos
- Análise comportamental
- Segurança ofensiva controlada
- Visualização estilo SOC
