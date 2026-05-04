#!/bin/bash

echo "[+] Configurando proteção local do GuiPhish..."

cat > .gitignore <<EOF
fotos/
logs/
relatorios/

*.jpg
*_info.json
eventos.jsonl
EOF

mkdir -p fotos logs relatorios

chmod 700 fotos logs relatorios

echo "[+] .gitignore criado/atualizado."
echo "[+] Pastas locais protegidas com chmod 700."
echo "[+] Configuração concluída."
