# Claude Pi Portal 🍓

Web-GUI til at køre Python-scripts med Claude AI på en Raspberry Pi.

## Krav
- Raspberry Pi 4 eller 5 (ARM64)
- Raspberry Pi OS 64-bit (Bookworm)
- Docker + Docker Compose
- Mindst 16 GB SD-kort / SSD til /opt/claude-data

---

## Opsætning (3 trin)

### 1. Installer Docker på Pi'en
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Klargør data-mappen (10 GB begrænset med quota)
```bash
sudo mkdir -p /opt/claude-data
sudo chown $USER:$USER /opt/claude-data
# Hvis du bruger en ekstern SSD, mount den her i stedet
```

### 3. Start portalen
```bash
cp .env.example .env
nano .env          # Indsæt din ANTHROPIC_API_KEY

docker compose up -d --build
```

Åbn **http://[pi-ip]:5000** i din browser.

---

## Brug

| Funktion | Beskrivelse |
|---|---|
| **Scripts sidebar** | Liste over alle .py filer i /data/scripts |
| **Editor** | Skriv/rediger scripts direkte i browseren |
| **▶ Kør** | Gem + kør scriptet, output streames live |
| **Claude Chat** | Tal med Claude om dine scripts/opgaver |
| **Stats-bar** | CPU, RAM og diskforbrug i realtid |

---

## Tilføj egne scripts

Du kan enten:
- Oprette via portalen (klik **+ Ny**)
- Kopiere .py-filer direkte til `./scripts/` mappen på Pi'en

Scripts har adgang til miljøvariablen `ANTHROPIC_API_KEY` automatisk.

---

## Opdater
```bash
git pull
docker compose up -d --build
```

## Stop
```bash
docker compose down
```

## Logs
```bash
docker compose logs -f
```

---

## Mappestruktur
```
claude-pi/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                  ← Din API-nøgle (laves fra .env.example)
├── scripts/              ← Dine Python-scripts (synkroniseres til container)
├── logs/                 ← Kørselslogs
└── app/
    ├── main.py           ← Flask-app
    └── templates/
        └── index.html    ← Web-GUI
```
