# GuiPhish 🔐

Ferramenta educacional para laboratório de conscientização em segurança, demonstrando riscos associados a permissões de navegador, geolocalização e engenharia social.

---

## 🎯 Objetivo

Simular um cenário controlado onde o usuário concede permissões sensíveis do navegador, como câmera, localização e informações de e-mail, demonstrando como decisões aparentemente simples podem levar à exposição de dados.

---

## ⚙️ Tecnologias

- HTML
- JavaScript
- Python
- Flask
- Flask-CORS
- Cloudflared
- Kali Linux

---

## 🔄 Fluxo de funcionamento

1. O servidor Flask é iniciado no Kali Linux
2. O usuário escolhe um modo no menu da ferramenta
3. O Cloudflared gera um link HTTPS temporário
4. O usuário acessa o link
5. A página apresenta opções de simulação
6. A câmera pode ser testada e a foto salva localmente em `fotos/`
7. A localização pode ser testada e registrada em `logs/eventos.jsonl`
8. A simulação de e-mail/conta fica disponível em `/email`
9. Relatórios podem ser gerados em `relatorios/`
10. A simulação é finalizada sem exposição pública dos arquivos locais

---

## 🐍 Backend Flask

O Flask é responsável por:

- Servir o arquivo `index.html`
- Servir a página separada `email.html`
- Receber eventos via requisição POST em `/evento`
- Receber imagens via requisição POST em `/capture`
- Decodificar imagens em Base64
- Salvar fotos no diretório `fotos/`
- Registrar logs e metadados em `logs/eventos.jsonl`
- Gerar relatórios locais em `relatorios/`

---

## 🧪 Instalação e execução

### 1. Atualizar o sistema

```bash
sudo apt update
```

### 2. Instalar dependências
```bash
sudo apt install python3-flask python3-flask-cors -y
```

### 3. Acessar o projeto
```bash
git clone https://github.com/geovanniandrade/verificacao-seguranca.git
cd /home/kali/verificacao-seguranca
```
### 4. Executar o servidor Flask
```bash
python3 server.py
```
### 5. Escolher uma opção no menu
```bash
1) 📸 Testar permissão de câmera
2) 🌍 Testar permissão de localização
3) 📊 Dashboard / visualizar logs
4) 🧾 Gerar relatório do lab
5) 🧹 Limpar evidências locais
6) 📧 Simulação de e-mail/conta
7) 🛑 Sair
6. Saída esperada
```
```bash
Running on http://127.0.0.1:10000
Running on http://SEU-IP:10000
```

### 🌐 Expor o lab com HTTPS

Em outro terminal:
```bash
cloudflared tunnel --url http://127.0.0.1:10000 --protocol http2
```
O Cloudflared irá gerar um link temporário:
```bash
https://exemplo.trycloudflare.com
```
### 📧 Simulação de e-mail/conta

A simulação de e-mail fica em uma página separada.

Acesse:
```bash
https://SEU-LINK.trycloudflare.com/email

A simulação registra apenas o domínio informado, sem coletar senha, MFA, tokens ou dados sensíveis.
```
### 📸 Validar fotos capturadas
```bash
ls -la fotos
```
Para abrir a pasta:

xdg-open fotos

### 🌍 Validar logs e localização
```bash
tail -n 10 logs/eventos.jsonl
```
### 🧾 Gerar relatório do lab

No menu da ferramenta, selecione:
```bash
4
```
Os relatórios serão salvos em:
```bash
relatorios/
```
### 🧹 Limpar evidências locais

No menu da ferramenta, selecione:
```bash
5
```

Essa opção apaga fotos, logs e relatórios locais após confirmação.


### ⚠️ Uso ético

Este projeto deve ser utilizado exclusivamente em ambientes controlados, acadêmicos ou corporativos, com consentimento dos participantes.

Nunca utilize esta ferramenta para capturar imagens, localização, e-mails ou qualquer dado sem autorização explícita.

### 🛡️ Aprendizados
Engenharia social aplicada
Permissões de navegador
WebRTC
Geolocalização via browser
Backend com Flask
Registro de eventos
Geração de relatórios
Exposição segura via túnel HTTPS
Boas práticas de conscientização em segurança
