#!/bin/sh
# ============================================================
# ssh-notify.sh — Notification ntfy à chaque connexion SSH
#
# INSTALLATION :
#   sudo cp ssh-notify.sh /etc/ssh/sshrc
#   sudo chmod +x /etc/ssh/sshrc
#
# Ce fichier est exécuté automatiquement par sshd pour
# chaque nouvelle connexion interactive.
# ============================================================

NTFY_URL="https://ntfy.balezeau.fr"
NTFY_TOPIC="ssh-connection"
NTFY_TOKEN=$(cat /etc/ssh/ntfy_token 2>/dev/null)   # fichier créé via : echo "TOKEN" > /etc/ssh/ntfy_token && chmod 600 /etc/ssh/ntfy_token

# Infos de connexion
IP=$(echo "$SSH_CONNECTION" | awk '{print $1}')
PORT=$(echo "$SSH_CONNECTION" | awk '{print $4}')
DATE=$(date '+%d/%m/%Y à %H:%M:%S')
HOST=$(hostname)

curl -sf \
  -H "Authorization: Bearer ${NTFY_TOKEN}" \
  -H "Title: [NAS] Connexion SSH" \
  -H "Priority: high" \
  -d "Utilisateur : ${USER}
IP : ${IP}
Heure : ${DATE}
Serveur : ${HOST}" \
  "${NTFY_URL}/${NTFY_TOPIC}" > /dev/null 2>&1 &
# Le & évite de bloquer l'ouverture du terminal si ntfy est inaccessible
