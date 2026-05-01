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

```bash
sudo apt update
