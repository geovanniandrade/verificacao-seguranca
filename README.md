# GuiPhish 🔐

Ferramenta educacional para laboratório de conscientização em segurança, demonstrando riscos associados a permissões de navegador e engenharia social.

## 🎯 Objetivo

Simular um cenário controlado onde o usuário concede permissão de câmera em uma página web, permitindo demonstrar como permissões concedidas sem atenção podem gerar exposição de dados.

## ⚙️ Tecnologias

- HTML
- JavaScript
- Python
- Flask
- Cloudflared
- Kali Linux

## 🔄 Fluxo de funcionamento

1. O servidor Flask é iniciado no Kali.
2. O Cloudflared gera um link HTTPS temporário.
3. O usuário acessa o link.
4. A página solicita permissão da câmera.
5. Após autorização, a imagem é capturada.
6. A foto é enviada ao Flask.
7. O arquivo é salvo localmente na pasta `fotos/`.

## 🧪 Execução

```bash
python3 server.py
