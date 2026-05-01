# GuiPhish 🔐

Ferramenta educacional para laboratório de conscientização em segurança, demonstrando riscos associados a permissões de navegador e engenharia social.

---

## 🎯 Objetivo

Simular um cenário controlado onde o usuário concede permissão de câmera em uma página web, demonstrando como decisões aparentemente simples podem levar à exposição de dados sensíveis.

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
4. A página solicita permissão da câmera  
5. Após autorização, a imagem é capturada automaticamente  
6. A foto é enviada ao backend Flask  
7. O arquivo é salvo localmente na pasta `fotos/`  
8. A simulação é finalizada sem exposição pública das imagens  

---

## 🐍 Backend Flask

O Flask é responsável por:

- Servir o arquivo `index.html`
- Receber a imagem capturada via requisição POST (`/capture`)
- Decodificar a imagem (Base64)
- Salvar a foto no diretório `fotos/`
- Registrar informações básicas (IP, user-agent, timestamp)

---

## 🧪 Instalação e execução

### 1. Atualizar o sistema
### 2. sudo apt install python3-flask python3-flask-cors -y
### 3. cd /home/kali/verificacao-seguranca
### 4. python3 server.py
SAIDA ESPERADA
Running on http://127.0.0.1:10000
Running on http://SEU-IP:10000

Em outro terminal:
### cloudflared tunnel --url http://127.0.0.1:10000 --protocol http2

Para validar as informações:
### ls -la fotos

```bash
sudo apt update
