# GuiPhish 🔐

Ferramenta educacional para laboratório de conscientização em segurança, demonstrando riscos associados a permissões de navegador, geolocalização e engenharia social.

---

## 🎯 Objetivo

Simular um cenário controlado onde o usuário concede permissões sensíveis do navegador, como câmera e localização, demonstrando como decisões aparentemente simples podem levar à exposição de dados.

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
2. O Cloudflared gera um link HTTPS temporário
3. O usuário acessa o link
4. A página apresenta opções de simulação
5. O usuário pode testar permissão de câmera ou localização
6. A foto é salva localmente na pasta `fotos/`
7. Os eventos e dados de localização são registrados em `logs/eventos.jsonl`
8. A simulação é finalizada sem exposição pública dos arquivos

---

## 🐍 Backend Flask

O Flask é responsável por:

- Servir o arquivo `index.html`
- Receber eventos via requisição POST em `/evento`
- Receber imagens via requisição POST em `/capture`
- Decodificar imagens em Base64
- Salvar fotos no diretório `fotos/`
- Registrar logs e metadados em `logs/eventos.jsonl`

---

## 🧪 Instalação e execução

### 1. Atualizar o sistema

```bash
sudo apt update
```
### 2. sudo apt install python3-flask python3-flask-cors -y
### 3. cd /home/kali/verificacao-seguranca
### 4. python3 server.py
```bash
Running on http://127.0.0.1:10000
Running on http://SEU-IP:10000
```
### 5. cloudflared tunnel --url http://127.0.0.1:10000 --protocol http2
```bash
O Cloudflared irá gerar um link temporário:
https://exemplo.trycloudflare.com
```
### 📸 Validar fotos capturadas
ls -la fotos
```bash
Para abrir a pasta:
xdg-open fotos
```
### 🌍 Validar logs e localização

tail -n 10 logs/eventos.jsonl

### ⚠️ Uso ético

Este projeto deve ser utilizado exclusivamente em ambientes controlados, acadêmicos ou corporativos, com consentimento dos participantes.

Nunca utilize esta ferramenta para capturar imagens, localização ou qualquer dado sem autorização explícita.
