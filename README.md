# Veu Transcriber

Aplicación de transcripción de vídeo mediante lectura de labios (*lip reading*). Combina un backend de inferencia en Python con un frontend web en Angular.

## Arquitectura

```
veu-transcriber/
├── backend-python/     # API FastAPI + modelo de lip reading (Auto-AVSR)
├── frontend-angular/   # SPA Angular para subir vídeos y ver la transcripción
└── docker-compose.yml  # Orquestación de ambos servicios
```

| Servicio  | Puerto | Descripción |
|-----------|--------|-------------|
| Backend   | 8000   | API REST (FastAPI + modelo VSR) |
| Frontend  | 80     | Interfaz web servida por nginx |

## Requisitos

- [Docker](https://www.docker.com/) y Docker Compose

## Puesta en marcha

```bash
docker compose up --build
```

Abre el navegador en `http://localhost` para usar la aplicación.

> La primera vez que se construya el backend se descargará el modelo de pesos (~1 GB). Ten paciencia.

## Desarrollo local (sin Docker)

Consulta los READMEs individuales de cada proyecto:

- [backend-python/README.md](backend-python/README.md)
- [frontend-angular/README.md](frontend-angular/README.md)
