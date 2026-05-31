# LiLNasX — Homelab Docker Stack

Stack self-hosted complète tournant sur un NAS, orchestrée avec Docker Compose.  
Reverse proxy Traefik + SSO Authentik + une vingtaine de services.

---

## Architecture

```
Internet
   │
   ▼
Traefik (reverse proxy TLS + Let's Encrypt)
   │
   ├── Socket Proxy (accès Docker sécurisé)
   ├── Authentik (SSO — protège les services exposés)
   └── Services (voir liste ci-dessous)

PostgreSQL (base partagée : Authentik, Immich)
```

Tous les services communiquent via des réseaux Docker isolés (`treafik_proxy`, `socket_proxy`, `postgres_backend`, etc.).  
Les volumes persistants sont déclarés `external: true` et créés manuellement avant le déploiement.

---

## Services

### Core
| Service | Image | Rôle |
|---|---|---|
| Traefik | `traefik:latest` | Reverse proxy, TLS, ACME |
| Socket Proxy | `tecnativa/docker-socket-proxy` | Proxy sécurisé sur `/var/run/docker.sock` |
| PostgreSQL | `postgres` | Base de données partagée |
| Authentik | `ghcr.io/goauthentik/server` | SSO / Identity Provider |

### Infra
| Service | Image | Rôle |
|---|---|---|
| Portainer | `portainer/portainer-ce` | Interface de gestion Docker |
| WireGuard (wg-easy) | `ghcr.io/wg-easy/wg-easy` | VPN WireGuard |
| Cloudflare DDNS | `favonia/cloudflare-ddns` | Mise à jour DNS dynamique |
| Ntfy | `binwiederhier/ntfy` | Notifications push |
| Uptime Kuma | `louislam/uptime-kuma` | Monitoring / status page |

### Applications
| Service | Image | Rôle |
|---|---|---|
| Vaultwarden | `vaultwarden/server` | Gestionnaire de mots de passe (Bitwarden) |
| Syncthing | `syncthing/syncthing` | Synchronisation de fichiers |
| Nginx | `nginx` | Serveur web (portfolio) |
| Stalwart | `stalwartlabs/stalwart` | Serveur mail (SMTP/IMAP/JMAP) |
| Bulwark | `ghcr.io/bulwarkmail/webmail` | Webmail |
| Immich | `ghcr.io/immich-app/immich-server` | Gestion de photos / vidéos |
| Gluetun | `qmcgaw/gluetun` | VPN client (CyberGhost) |

### Jeux
| Service | Rôle |
|---|---|
| Minecraft | Serveur Minecraft |
| Valheim | Serveur Valheim + BepInEx |
| Core Keeper | Serveur Core Keeper |

---

## Déploiement

### Prérequis

- Docker + Docker Compose v2
- Créer les volumes externes avant le premier démarrage :

```bash
docker volume create postgres-data
docker volume create authentik-redis
docker volume create traefik_certs
docker volume create portainer_data
docker volume create wg-easy-data
docker volume create uptime-kuma
docker volume create vaultwarden-data
docker volume create stalwart-etc
docker volume create stalwart-data
docker volume create ntfy-data
docker volume create gluetun
docker volume create immich-model-cache
docker volume create portfolio-data
docker volume create bulwark-settings
docker volume create bulwark-admin
docker volume create bulwark-admin-state
docker volume create bulwark-telemetry
```

### Variables d'environnement

Chaque service possède son propre fichier `.env` (non versionné).  
Copier les templates et les remplir :

```bash
cp authentik/.env.example authentik/.env
cp postgres/.env.example postgres/.env
# etc.
```

Les fichiers `.env.example` contiennent toutes les variables requises avec des valeurs vides ou de démonstration.

### Lancement

```bash
# Démarrer toute la stack
docker compose up -d

# Démarrer un seul service
docker compose up -d traefik

# Voir les logs
docker compose logs -f traefik
```

---

## Structure du repo

```
.
├── docker-compose.yml          # Compose principal (includes tous les services)
├── traefik/
│   └── rules/                  # Middlewares & chaînes d'auth Traefik
├── authentik/                  # Config Authentik
├── postgres/
│   └── init/                   # Scripts d'init SQL
├── nginx/
│   └── conf.d/                 # Virtual hosts Nginx
├── ntfy/
│   ├── server.yml              # Config Ntfy
│   └── ssh-notify.sh           # Hook SSH → notification
└── [service]/
    └── docker-compose.yml      # Compose de chaque service
```

---

## Sécurité

- Toutes les variables sensibles sont dans des fichiers `.env` non versionnés.
- Les secrets Docker (tokens Cloudflare) sont injectés via `secrets:`.
- Le socket Docker n'est jamais monté directement — il passe par Socket Proxy.
- Traefik force HTTPS avec redirection 301 et headers de sécurité stricts.
- Les services sensibles sont protégés par Authentik (ForwardAuth).
