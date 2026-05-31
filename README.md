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
